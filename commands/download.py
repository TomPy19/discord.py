from pytube import YouTube

async def downloadYouTube(videourl):
    yt = YouTube(videourl)
    print (yt.streams.filter(only_audio=True)[0].download('tmp', f'{yt.title}.mp3'))
    return yt.title