import discord
from discord.ext import commands
import os

import requests
import discord
import asyncio

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
API_TOKEN = 'YOUR_TSHOCK_API_TOKEN'
API_URL = 'http://localhost:7878/v2/players'

intents = discord.Intents.default()
client = discord.Client(intents=intents)

prev_deaths = {}

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = discord.utils.get(client.get_all_channels(), name='terraria-updates')

    while True:
        response = requests.get(API_URL, headers={"Authorization": f"Bearer {API_TOKEN}"})
        data = response.json()

        for player in data.get("players", []):
            name = player.get("name")
            deaths = player.get("deaths", 0)

            if name not in prev_deaths:
                prev_deaths[name] = deaths
            elif deaths > prev_deaths[name]:
                await channel.send(f"💀 {name} just died! Total deaths: {deaths}")
                prev_deaths[name] = deaths

        await asyncio.sleep(5)

client.run(TOKEN)