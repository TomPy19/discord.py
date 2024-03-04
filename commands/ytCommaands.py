import pytube

async def getTitle(videourl):
  yt = pytube.YouTube(videourl)
  return yt.title