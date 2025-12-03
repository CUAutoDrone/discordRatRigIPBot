import discord
import os
import subprocess

token = os.environ.get("API_TOKEN")

intents = discord.Intents.none()
intents.message_content = True
intents.messages = True

ipBot = discord.Client(intents=intents)
current_channel = int(os.environ.get("IPs_CHANNEL"))

@ipBot.event
async def on_ready():
    print("Bot is ready.")
    hostname = subprocess.check_output("hostname -A", shell=True, text=True)
    hostname = hostname.rstrip()
    try:
        with open(".discord_ip_file", "r", encoding='utf-8') as prev_ip_file:
            prev_hostname = prev_ip_file.read().rstrip()
    except FileNotFoundError:
        prev_hostname = ""
    if hostname != prev_hostname:
        mes = await ipBot.fetch_channel(current_channel)
        mes_to_send = "The Rat Rig's new address is: " + hostname
        new_message = await mes.send(mes_to_send)
        async for old_message in mes.pins():
            if old_message.author.id == ipBot.user.id:
                await old_message.unpin()
        await new_message.pin()
        with open(".discord_ip_file", "w", encoding="utf-8") as current_ip_file:
            current_ip_file.write(hostname)


@ipBot.event
async def on_message(message):
    if ipBot.user.id in [mention.id for mention in message.mentions]:
        hostname = subprocess.check_output("hostname -A", shell=True, text=True)
        hostname = hostname.rstrip()
        mes = await ipBot.fetch_channel(current_channel)
        mes_to_send = "The Rat Rig's address is " + hostname
        new_message = await message.reply(mes_to_send)
        async for old_message in mes.pins():
            if old_message.author.id == ipBot.user.id:
                await old_message.unpin()
        await new_message.pin()
        with open(".discord_ip_file", "w", encoding='utf-8') as current_ip_file:
            current_ip_file.write(hostname)

ipBot.run(token)
