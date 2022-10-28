from pytube import YouTube


def yt_video_download(url: str):
    path = "./cache"
    try:
        yt = YouTube(url).streams
    except:
        print("Connection error")
        return False
    data = yt.get_highest_resolution()
    try:
        data.download(path)
        print("Download completed")
        return True
    except:
        print("Download error")
        return False


def yt_audio_download(url: str):
    path = "./cache"
    try:
        yt = YouTube(url).streams
    except:
        print("Connection error")
        return False
    data = yt.get_audio_only()
    try:
        data.download(path)
        print("Download completed")
        return True
    except:
        print("Download error")
        return False
