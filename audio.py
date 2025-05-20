import os
from moviepy.editor import *
from faster_whisper import WhisperModel
from dotenv import load_dotenv
from logger import logger

load_dotenv()

class Audio:
    def extract(video_path):
        """Extracts the audio from a video and saves it in wav format"""
        logger.info(f"\nExtracting audio from video: {video_path}")
        
        video_path = video_path.replace("'", "")
        
        logger.debug(f'video_path = {video_path}')
        
        output_path = os.path.dirname(video_path)
        output_path = output_path.replace('videos', 'audios')
        logger.debug(f'output_path = {output_path}')
        
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        logger.debug(f'basename= {base_name}')
        
        audio_path = f'{output_path}/{base_name}.mp3'
        logger.debug(f'audio_path = {audio_path}')
        
        video = VideoFileClip(output_path)
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            logger.info(f"Creating Folder {output_path}")
            
        video.audio.write_audiofile(audio_path)
        
        logger.info(f'Audio saved in: {audio_path}')
        return audio_path
    
    
    def transcription(audio_path: str) -> str:
        """Transcribe an audio file saved in audio_path to text using speech recognition"""
        logger.info(f"Transcribing audio: {audio_path}")
        
        audio_path = audio_path.replace("'", "")
        model = WhisperModel("medium")
        
        result = model.transcribe(audio_path, language = 'pt')
        
        transcription = ""
        
        for segment in result[0]:
            transcription += segment.text + " "
            
        output_path = os.path.dirname(audio_path)
        output_path = output_path.replace('audios', 'transcription')
        base_name = os.path.splitext(os.path.basename{audio_path})[0]
        transcription_path = f'{output_path}/{base_name}.md'
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            logger.info(f"Creating Folder '{output_path}'")
            
        with open(transcription_path, 'w', encoding='utf-8') as f:
            f.write(transcription.strip())
            
        logger.info(f'Transcription save in: {transcription_path}')
        return transcription_path
    

if __name__ == '__main__':
    video_path = ''
    video_path = ''
    audio_path = Audio.extract(video_path)
    transcription = Audio.transcription(audio_path)