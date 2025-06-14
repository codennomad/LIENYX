import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import subprocess
from faster_whisper import WhisperModel
from dotenv import load_dotenv
from lienyx.logger import logger
import re
import aiofiles

load_dotenv()

executor = ThreadPoolExecutor()

class Audio:
    @staticmethod
    async def extract(video_path):
        """Extracts the audio from a video and saves it in mp3 format asynchronously using FFmpeg."""
        try:
            logger.info(f"Extraindo áudio de: {video_path} usando FFmpeg")

            # Corrige caminho quebrado que veio sem separador
            if not os.path.exists(video_path):
                dir_name = "_downloads_telegram"
                file_name = video_path.replace("_downloads_telegram", "").lstrip("/\\")
                tentative_path = os.path.join(dir_name, file_name)

                if os.path.exists(tentative_path):
                    logger.warning(f"Caminho corrigido automaticamente de {video_path} para {tentative_path}")
                    video_path = tentative_path
                else:
                    raise FileNotFoundError(f"Arquivo não encontrado: {video_path} nem {tentative_path}")

            audios_base_dir = "_audios"
            original_base_name = os.path.splitext(os.path.basename(video_path))[0]

            # Sanitize nome do arquivo
            sanitized_base_name = re.sub(r'[^\w\-. ()]', '_', original_base_name)
            sanitized_video_path = os.path.join(os.path.dirname(video_path), f"{sanitized_base_name}.mp4")

            # Renomeia fisicamente se necessário
            if video_path != sanitized_video_path:
                os.rename(video_path, sanitized_video_path)
                logger.debug(f"Arquivo renomeado de {video_path} para {sanitized_video_path}")
                video_path = sanitized_video_path

            output_dir = os.path.join(audios_base_dir)
            audio_path = os.path.join(output_dir, f'{sanitized_base_name}.mp3')

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logger.debug(f"Criando pasta: {output_dir}")

            command = [
                'ffmpeg',
                '-i', video_path,
                '-vn',
                '-acodec', 'libmp3lame',
                '-q:a', '2',
                audio_path
            ]

            logger.debug(f"Executando comando FFmpeg: {' '.join(command)}")

            loop = asyncio.get_running_loop()
            process = await loop.run_in_executor(
                executor,
                lambda: subprocess.run(command, capture_output=True, text=True, check=True)
            )

            if process.returncode != 0:
                logger.error(f"Erro FFmpeg ao extrair áudio. Stdout: {process.stdout} Stderr: {process.stderr}")
                raise Exception(f"FFmpeg extraction failed: {process.stderr}")

            logger.info(f'Áudio salvo em: {audio_path}')
            return audio_path
        except Exception as e:
            logger.exception("Erro ao extrair áudio")
            raise e

    @staticmethod
    async def transcription(audio_path: str) -> str:
        """Transcribe an audio file to text using speech recognition asynchronously."""
        try:
            logger.info(f"Transcrevendo áudio: {audio_path}")
            audio_path = audio_path.replace("'", "")

            # Corrige caminho quebrado
            if not os.path.exists(audio_path):
                dir_name = "_audios"
                file_name = audio_path.replace("_audios", "").lstrip("/\\")
                tentative_path = os.path.join(dir_name, file_name)

                if os.path.exists(tentative_path):
                    logger.warning(f"Caminho corrigido automaticamente de {audio_path} para {tentative_path}")
                    audio_path = tentative_path
                else:
                    raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path} nem {tentative_path}")
            
            
            logger.debug("Carregando modelo Whisper 'medium'...")
            model = WhisperModel("medium") 
            logger.debug("Modelo Whisper carregado.")
            logger.info("A transcrição pode levar vários minutos, dependendo do tamanho do áudio e do hardware.")

            logger.debug(f"Iniciando transcrição do áudio: {audio_path}")
            loop = asyncio.get_running_loop()
            segments = await loop.run_in_executor(executor, Audio._sync_transcribe, model, audio_path)
            logger.debug("Transcrição do áudio concluída.")

            transcription = " ".join([segment.text for segment in segments])

            transcription_base_dir = "_transcriptions"
            output_dir = os.path.join(transcription_base_dir)
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            transcription_path = os.path.join(output_dir, f'{base_name}.md')

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logger.debug(f"Criando pasta: {output_dir}")

            async with aiofiles.open(transcription_path, 'w', encoding='utf-8') as f:
                await f.write(transcription.strip())

            logger.success(f'Transcrição salva em: {transcription_path}') # Usar logger.success para indicar sucesso na transcrição
            return transcription_path
        except Exception as e:
            logger.exception("Erro ao transcrever áudio")
            raise e

    @staticmethod
    def _sync_transcribe(model, audio_path):
        segments, _ = model.transcribe(audio_path, language='pt')
        return list(segments)

if __name__ == '__main__':
    pass