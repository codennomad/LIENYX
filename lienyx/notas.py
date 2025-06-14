import os
import asyncio
import aiofiles  # Importar aiofiles para operações de arquivo assíncronas
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from lienyx.logger import logger

load_dotenv()

llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model='gpt-4o-mini',
    temperature=0
)

class Notas:
    @staticmethod
    async def create_tags(text):
        try:
            logger.info('Criando tags assincronamente...')
            tags = await llm.ainvoke(
                f'Crie ate 10 tags referentes a este texto: \n{text}\n'
                f'Voce deve responder apenas as tags, sem nenhum comentario, nem numeracao. '
                f'As tags devem estar alinhadas em uma unica linha, separadas por um espaco. '
                f'Todas devem comecar com # e estar relacionadas ao conteudo.'
            )
            return tags.content
        except Exception as e:
            logger.exception("Erro ao criar tags")
            raise e

    @staticmethod
    async def create_short_summary(text):
        try:
            logger.info('Criando resumo curto assincronamente...')
            short_summary = await llm.ainvoke(
                f'Crie um resumo do texto em 20 palavras: \n{text}'
            )
            return short_summary.content
        except Exception as e:
            logger.exception("Erro ao criar resumo curto")
            raise e

    @staticmethod
    async def create_detailed_summary(text):
        try:
            logger.info('Criando resumo detalhado assincronamente...')
            detailed_summary = await llm.ainvoke(
                f'Resuma detalhadamente o texto: \n{text}\n'
                f'Mantenha todas as informacoes importantes de forma estruturada.'
            )
            return detailed_summary.content
        except Exception as e:
            logger.exception("Erro ao criar resumo detalhado")
            raise e

    @staticmethod
    async def create_bullet_point(text):
        try:
            logger.info('Criando bullet points assincronamente...')
            bullet_point = await llm.ainvoke(
                f'Liste em bullet points as principais ideias referentes ao texto: \n{text}'
            )
            return bullet_point.content
        except Exception as e:
            logger.exception("Erro ao criar bullet points")
            raise e

    @staticmethod
    def format_note(tags, short_summary, detailed_summary, bullet_point):
        try:
            logger.info('Formatando nota final...')
            final_text = (
                f'{tags}\n\n'
                f'# Resumo do Vídeo\n\n'
                f'## Resumo Curto\n{short_summary}\n\n'
                f'## Resumo Detalhado\n{detailed_summary}\n\n'
                f'## Bullet Points\n{bullet_point}\n\n'
            )
            return final_text
        except Exception as e:
            logger.exception("Erro ao formatar nota")
            raise e

    @staticmethod
    async def save_note(transcription_path):
        try:
            logger.info('Criando nota a partir da transcrição assincronamente')
            transcription_path = transcription_path.replace("'", "")
            logger.debug(f'transcription_path = {transcription_path}')

            # Correção de caminho quebrado
            if not os.path.exists(transcription_path):
                dir_name = "_transcriptions"
                file_name = transcription_path.replace("_transcriptions", "").lstrip("/\\")
                tentative_path = os.path.join(dir_name, file_name)

                if os.path.exists(tentative_path):
                    logger.warning(f"Caminho corrigido automaticamente de {transcription_path} para {tentative_path}")
                    transcription_path = tentative_path
                else:
                    raise FileNotFoundError(f"Arquivo de transcrição não encontrado: {transcription_path} nem {tentative_path}")

            async with aiofiles.open(transcription_path, 'r', encoding='utf-8') as file:
                transcription = await file.read()

            tags = await Notas.create_tags(transcription)
            short_summary = await Notas.create_short_summary(transcription)
            detailed_summary = await Notas.create_detailed_summary(transcription)
            bullet_point = await Notas.create_bullet_point(transcription)

            nota = Notas.format_note(tags, short_summary, detailed_summary, bullet_point)

            notes_base_dir = "_notes"
            output_dir = os.path.join(notes_base_dir)
            os.makedirs(output_dir, exist_ok=True)
            logger.debug(f"Pasta de notas: {output_dir}")

            base_name = os.path.splitext(os.path.basename(transcription_path))[0]
            summary_path = os.path.join(output_dir, f'{base_name}.md')

            async with aiofiles.open(summary_path, 'w', encoding='utf-8') as f:
                await f.write(nota)

            logger.info(f'Nota salva em: {summary_path}')
            return summary_path
        except Exception as e:
            logger.exception("Erro ao salvar nota")
            raise e

if __name__ == '__main__':
    pass
