import asyncio
import os
import tempfile

import discord
import pyautogui
import pygame
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
screamer_lock = asyncio.Lock()


def screamer(photo, sound, duration=2000):
    try:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        w, h = screen.get_size()
        img = pygame.transform.scale(pygame.image.load(photo), (w, h))
        screen.blit(img, (0, 0))
        pygame.display.flip()

        end = pygame.time.get_ticks() + duration
        while pygame.time.get_ticks() < end:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            pygame.time.wait(10)
    finally:
        if pygame.mixer.get_init():
            pygame.mixer.music.unload()
        pygame.quit()


def use_touch(touch="z"):
    pyautogui.press(touch)


class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()  # enregistre /screamer auprès de Discord


bot = MyBot(command_prefix="!", intents=discord.Intents.default())


@bot.tree.command(name="screamer", description="Lance un screamer avec une image et un son")
@app_commands.describe(image="Image à afficher", son="Fichier audio")
async def scream(interaction: discord.Interaction,
                 image: discord.Attachment,
                 son: discord.Attachment):
    await interaction.response.defer(ephemeral=True)
    if not (image.content_type or "").startswith("image/"):
        return await interaction.followup.send("Le premier fichier doit être une image.")
    if not (son.content_type or "").startswith("audio/"):
        return await interaction.followup.send("Le second fichier doit être un audio.")

    img_path = snd_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[1]) as f:
            img_path = f.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(son.filename)[1]) as f:
            snd_path = f.name

        await image.save(img_path)
        await son.save(snd_path)

        async with screamer_lock:
            await asyncio.to_thread(screamer, img_path, snd_path)
        await interaction.followup.send("Screamer lancé !")
    except Exception as e:
        await interaction.followup.send(f"Erreur : {e}")
    finally:
        for p in (img_path, snd_path):
            if p and os.path.exists(p):
                os.remove(p)

@bot.tree.command(name="command", description="fais moi utiliser la touche que tu veux")
async def command(interaction: discord.Interaction, touch: str):
    try:
        use_touch(touch)
        await interaction.followup.send("touche lancée !")
    except Exception as e:
        await interaction.followup.send(f"Erreur : {e}")

bot.run(os.getenv("KEY"))
