from editdistance import distance
import discord
from datetime import timedelta
from private_info import token, usernames_to_check, words_to_ban

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if str(message.author) not in usernames_to_check:
        return
    
    to_parse = message.content.lower()
    parsed_words = to_parse.strip('-_').split(' ')
    for word in words_to_ban:
        if word in to_parse:
            await message.author.timeout(timedelta(minutes = 10))
            await message.channel.send(f"{message.author} was banned for using the word {word}!")
            return
        for parsed in parsed_words:
            if distance(parsed, word) < 4:
                await message.author.timeout(timedelta(minutes = 10))
                await message.channel.send(f"{message.author} was banned for using {parsed} in place of {word}!")
                return

client.run(token)