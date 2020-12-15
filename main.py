import sys
from moviepy.editor import *
from pytube import YouTube
from moviepy.editor import AudioFileClip
import youtube_dl

video_url = 'downloads/video'
audio_url = 'downloads/music'
 
def down_video(url):
    ydl_opts = {
        'outtmpl': './downloads/video/%(title)s.mp4'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
    return (video_title, video_url+'/'+video_title+'.mp4')

def down_music(url):
    title,a = down_video(url)
    audioclip = AudioFileClip(video_url+'/'+title+'.mp4')
    audioclip.write_audiofile(audio_url+'/'+title+'.wav')
    os.remove(video_url+'/'+title+'.mp4')
    return audio_url+'/'+title+'.wav'







