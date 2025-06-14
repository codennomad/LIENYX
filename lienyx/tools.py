import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import subprocess
from faster_whisper import WhisperModel
import base64
from io import BytesIO
from PIL import Image
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.tools import Tool
from pydantic import BaseModel, Field 

# Importações dos módulos internos (absolutas)
from lienyx.download_youtube import YoutubeDownloader
from lienyx.audio import Audio
from lienyx.notas import Notas
from lienyx.logger import logger
from lienyx.image import ProcessImage

load_dotenv()

# Instanciar o LLM uma vez (para ProcessImage e Notas)
llm_for_image_analysis = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model='gpt-4o-mini',
    temperature=0
)
llm_for_notas = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model='gpt-4o-mini',
    temperature=0
)

# --- DEFINIÇÃO DOS ESQUEMAS DE ARGUMENTOS COM PYDANTIC ---
class DownloadVideoArgs(BaseModel):
    link: str = Field(description="The YouTube video link to download.")

class ExtractArgs(BaseModel):
    video_path: str = Field(description="The local path to the video file.")

class TranscriptionArgs(BaseModel):
    audio_path: str = Field(description="The local path to the audio file.")

class ProcessImageArgs(BaseModel):
    image_path: str = Field(description="The local path to the image file.")

class SaveNoteArgs(BaseModel):
    transcription_path: str = Field(description="The local path to the transcription file (Markdown).")



class LIENYXTools:
    def __init__(self):
        self.youtube_downloader = YoutubeDownloader()
        self.process_image_instance = ProcessImage()

        self.download_video_tool = Tool.from_function(
            func=self.youtube_downloader.download_video,
            name="download_video",
            description="Baixa vídeo do YouTube a partir de um link e retorna o caminho do arquivo assincronamente.",
            coroutine=self.youtube_downloader.download_video,
            args_schema=DownloadVideoArgs 
        )

        self.extract_tool = Tool.from_function(
            func=Audio.extract,
            name="extract",
            description="Extrai o áudio de um arquivo de vídeo MP4 e retorna o caminho do áudio gerado assincronamente.",
            coroutine=Audio.extract,
            args_schema=ExtractArgs 
        )

        self.transcription_tool = Tool.from_function(
            func=Audio.transcription,
            name="transcription",
            description="Transcreve um arquivo de áudio e retorna o caminho do arquivo de transcrição assincronamente.",
            coroutine=Audio.transcription,
            args_schema=TranscriptionArgs 
        )

        self.process_image_tool = Tool.from_function(
            func=self.process_image_instance.openai_analysis,
            name="ProcessImage",
            description="Analisa o conteúdo de uma imagem e retorna o resultado textual da IA assincronamente.",
            coroutine=self.process_image_instance.openai_analysis,
            args_schema=ProcessImageArgs 
        )

        self.save_note_tool = Tool.from_function(
            func=Notas.save_note,
            name="save_note",
            description="Cria e salva uma nota formatada a partir da transcrição do vídeo assincronamente.",
            coroutine=Notas.save_note,
            args_schema=SaveNoteArgs 
        )