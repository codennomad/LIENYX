from langchain.tools import tool
from download_youtube import YoutubeDownloader
from audio import Audio
from notas import Notas
from image import ProcessImage

class LIENYXTools:
    @tool
    def download_video(link: str) -> str:
        """Download the video from a youtube link and extract the description"""
        video_path = YoutubeDownloader().download_video(link)
        return video_path
    
    
    @tool
    def extract(video_path):
        pass
    
    
    @tool
    def transcription(audio_path: str) -> str:
        pass
    
    
    @tool
    def ProcessImage(image_path):
        pass
    
    
    @tool
    def save_note(transcription_path):
        pass