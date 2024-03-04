import discord
import config
import os
from commands.ytCommaands import getTitle
from commands.download import downloadYouTube

# Set up Discord client with necessary intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
queue = {}

# Event handler for when the bot is ready
@client.event
async def on_ready():
    for each in os.listdir('tmp'):
        os.remove(f'tmp/{each}')
    print(f'We have logged in as {client.user}')

# Event handler for player updates
@client.event
async def on_player_update(before, after):
    print(f'Player updated from {before} to {after}')

# Event handler for voice state updates
@client.event
async def on_voice_state_update(member, before, after):
    print(f'Voice state updated for {member} from {before} to {after}')

# Event handler for deleted messages
@client.event
async def on_message_delete(message):
    print(f'Message deleted: "{message.content}"')

# Event handler for handling queue checks
def check_queue(ctx, vc):
    if queue[ctx.guild.id]:
        vc.play(queue[ctx.guild.id][0]['FFaudio'], after=lambda e: check_queue(ctx, vc))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.04
        cTitle = queue[ctx.guild.id][0]['title']
        del queue[ctx.guild.id][0]
        os.remove(f'tmp/{cTitle}.mp3')
    else:
        vc.disconnect()

@client.event
async def on_disconnect():
    for each in os.listdir('tmp'):
        os.remove(f'tmp/{each}')
    print('Bot has disconnected.')

# Event handler for incoming messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.content.startswith('.'):
        return

    if message.content == '.ping':
        await message.channel.send('pong')

    if message.content == '.help':
        await message.channel.send('Commands: .play <YouTube URL>, .stop, .leave')

    if message.content.startswith('.play'):
        if message.author.voice is None:
            await message.channel.send('You are not in a voice channel.')
        # elif message.guild.voice_client is not None:
        #     await message.channel.send('I am already in a voice channel.')
        elif len(message.content.split(' ')) == 1:
            await message.channel.send('Please provide a YouTube video URL.')
        elif len(message.content.split(' ')) > 2:
            await message.channel.send('Please provide only one YouTube video URL.')
        elif 'list' in message.content.split(' ')[1]:
            # await message.channel.send('I cannot play playlists at the moment.')
            
        else:
            video_url = message.content.split(' ')[1]
            title = await getTitle(video_url)
            dlmessage = await message.channel.send(f'Downloading audio for {title}...')
            await downloadYouTube(video_url)
            await message.channel.delete_messages([dlmessage])
            await message.channel.send(f'Adding {title} to queue...')
            audio = discord.FFmpegPCMAudio(f'tmp/{title}.mp3')
            # os.remove(f'tmp/{title}.mp3')
            if message.guild.id not in queue:
                queue[message.guild.id] = []
                queue[message.guild.id].append({'FFaudio': audio, 'title': title})
                vc = await message.author.voice.channel.connect(self_deaf=True)
                vc.play(audio, after=lambda e: check_queue(message, vc))
                vc.source = discord.PCMVolumeTransformer(vc.source)
                vc.source.volume = 0.04
            else:
                queue[message.guild.id].append({'FFaudio': audio, 'title': title})
            
    if message.content == '.pause':
        await message.channel.send('Pausing audio.')
        message.guild.voice_client.pause()

    if message.content == '.resume':
        await message.channel.send('Resuming audio.')
        message.guild.voice_client.resume()

    if message.content == '.skip':
        await message.channel.send('Skipping audio.')
        message.guild.voice_client.stop()

    if message.content == '.queue':
        if message.guild.id in queue:
            queueMessage = ''
            for i in range(len(queue[message.guild.id])):
                queueMessage = queueMessage + f'{i}. ' + queue[message.guild.id][i]['title'] + '\n'
            await message.channel.send(queueMessage)
        else:
            await message.channel.send('The queue is empty.')

    if message.content == '.clear':
        if message.guild.id in queue:
            queue[message.guild.id] = []
            await message.channel.send('The queue has been cleared.')
        else:
            await message.channel.send('The queue is already empty.')

    if message.content == '.stop':
        await message.channel.send('Stopping audio.')
        message.guild.voice_client.stop()
        message.guild.voice_client.pause()
    
    if message.content == '.leave':
        await message.channel.send('Leaving voice channel.')
        await message.guild.voice_client.disconnect()
        for each in os.listdir('tmp'):
            os.remove(f'tmp/{each}')

# Run the bot with the provided token
client.run(config.TOKEN)