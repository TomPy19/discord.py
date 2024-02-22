from pytube import YouTube
import os

async def downloadYouTube(videourl):
    yt = YouTube(videourl)
    print (yt.streams.filter(only_audio=True)[0].download('tmp', 'audio.mp3'))
    return

