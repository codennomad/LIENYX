import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from yt_dlp import YoutubeDL
from lienyx.logger import logger


executor = ThreadPoolExecutor()

class YoutubeDownloader:

    async def download_video(self, link: str) -> str:
        """Baixa vídeo do YouTube de forma assíncrona."""
        try:
            logger.info(f"🎬 Iniciando download do vídeo: {link}")

            loop = asyncio.get_event_loop()
            video_path = await loop.run_in_executor(
                executor, self._sync_download_video, link
            )

            logger.success(f"✅ Download concluído: {video_path}")
            return video_path

        except Exception as e:
            logger.exception("❌ Erro ao baixar vídeo do YouTube")
            raise e

    def _sync_download_video(self, link: str) -> str:
        """Parte síncrona do download com yt-dlp."""

        output_path = "_downloads_telegram"
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            logger.debug("🔍 Extraindo informações do vídeo...")
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)

            # Corrige extensão caso yt-dlp não retorne .mp4
            if not filename.endswith('.mp4'):
                filename = os.path.splitext(filename)[0] + '.mp4'

            logger.debug(f"📄 Arquivo salvo em: {filename}")
            return filename
