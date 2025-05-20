import os 
import re
from logger import logger
from pytube import YouTube

class YoutubeDownloader:
    def download_video(self, link=):
        logger.info(f"Downloading video from the link=''")
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        title_video = yt.title
        
        
        output_path = '_videos'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            logger.info(f"Criando pasta '{output_path}'")
            
        title = re.sub(r'[<>:"/\\|?"]', '', title_video)
        title = title.replace("'", "")
        title = title.strip().replace(' ', '_')
        title = f'_{title}.mp4'
        video_path = stream.download(output_path, title)
        logger.info(f"Downloading video '{title_video}' para '{video_path}'")
        video_path = f'{output_path}/{title}'
        logger.info(f"Video download in: {video_path}")
        return video_path    
    
    
if __name__ == '__main__':
    yt = YoutubeDownloader()
    youtube_link= ''
    youtube_link= ''
    yt.download_video(youtube_link)