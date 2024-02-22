import discord
from commands.download import downloadYouTube

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.content.startswith('.'):
        return

    if message.content == '.ping':
        await message.channel.send('pong')

    if message.content.startswith('.play'):
        video_url = message.content.split(' ')[1]
        # await message.channel.send(f'Playing {video_url}')
        await message.channel.send(f'Downloading audio...')
        await downloadYouTube(video_url)
        await message.channel.send(f'Playing audio...')
        audio = discord.FFmpegPCMAudio('tmp/audio.mp3')
        vc = await message.author.voice.channel.connect()
        vc.play(audio)
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.02
        
        # await message.channel.send(file=audio)
        # await message.channel.send(f'Downloaded {video_url}')
        # await message.channel.send_file('commands/temp/audio.mp3')
    
    if message.content == '.leave':
        await message.guild.voice_client.disconnect()

client.run('MTIwOTk2ODU3OTM1NzcxMjQ4NA.GnU-Ao.cTwCb8WwNNxxkXLAxFjJmGbxuNzpB8skDtLzSY')