import os
from time import sleep
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes # Para tipagem

# ALTERAR ESTAS IMPORTAÇÕES PARA ABSOLUTAS COM BASE NO PACOTE 'lienyx'
from lienyx.tools import LIENYXTools
from lienyx.logger import logger
from pydantic import BaseModel
# Se outras classes (Audio, YoutubeDownloader, Notas, ProcessImage)
# fossem importadas diretamente em main.py, elas seriam:
# from lienyx.audio import Audio
# from lienyx.download_youtube import YoutubeDownloader
# from lienyx.image import ProcessImage
# from lienyx.notas import Notas

load_dotenv()

class LIENYXTelegramBot:
    def __init__(self):
        logger.info("Inicializando LIENYX Bot para Telegram...")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

        self.llm = ChatOpenAI(
            openai_api_base="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model='google/gemini-flash-1.5',
            temperature=0
        )

        self.tool = LIENYXTools()
        self.agent, self.tools = self._create_agent()

        self.application = Application.builder().token(self.telegram_token).build()

        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
        self.application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL, self.handle_file_message))

    def _create_agent(self):
        try:
            logger.info("Criando agente e ferramentas...")
            tools = [
                self.tool.download_video_tool,
                self.tool.extract_tool,
                self.tool.process_image_tool,
                self.tool.transcription_tool,
                self.tool.save_note_tool
            ]

            prompt = ChatPromptTemplate.from_messages([
                ("system", """
                Seu nome é LIENYX, um assistente especializado em criar notas detalhadas e completas.
                Auxilia extraindo informações principais, organizando-as e formatando como Markdown em português.
                Mantenha controle dos resultados das ferramentas e incorpore-os às notas.
                """),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ])

            agent = create_tool_calling_agent(llm=self.llm, tools=tools, prompt=prompt)
            return agent, tools
        except Exception as e:
            logger.exception("Erro ao criar agente")
            raise e

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Olá! Eu sou LIENYX, seu assistente de notas. Me envie um link do YouTube, um vídeo ou uma imagem para eu processar e criar uma nota para você!")
        logger.info(f"Comando /start recebido de {update.effective_user.full_name}")

    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = update.message.text
        logger.info(f"Mensagem de texto recebida de {update.effective_user.full_name}: {msg}")
        await update.message.reply_text("Processando sua solicitação...")

        try:
            agent_executor = AgentExecutor.from_agent_and_tools(
                agent=self.agent,
                tools=self.tools,
                verbose=True,
            )
            result = await agent_executor.ainvoke({"input": msg})
            await update.message.reply_text(f"Resultado do processamento:\n{result['output']}")
            logger.info(f"Processamento de texto concluído para {update.effective_user.full_name}.")
        except Exception as e:
            logger.exception(f"Erro ao processar mensagem de texto de {update.effective_user.full_name}")
            await update.message.reply_text(f"Ocorreu um erro ao processar sua mensagem: {e}")

    async def handle_file_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        file_info = None
        file_name = None

        if update.message.video:
            file_info = await update.message.video.get_file()
            file_name = update.message.video.file_name or f"video_{file_info.file_unique_id}.mp4"
            logger.info(f"Vídeo recebido de {update.effective_user.full_name}: {file_name}")
            await update.message.reply_text("Vídeo recebido. Baixando e processando...")
        elif update.message.photo:
            file_info = await update.message.photo[-1].get_file()
            file_name = f"image_{file_info.file_unique_id}.jpg"
            logger.info(f"Imagem recebida de {update.effective_user.full_name}.")
            await update.message.reply_text("Imagem recebida. Baixando e processando...")
        elif update.message.document:
            file_info = await update.message.document.get_file()
            file_name = update.message.document.file_name
            logger.info(f"Documento recebido de {update.effective_user.full_name}: {file_name}")
            await update.message.reply_text(f"Documento '{file_name}' recebido. Baixando e processando...")

        if file_info:
            download_folder = "_downloads_telegram"
            os.makedirs(download_folder, exist_ok=True)
            file_path = os.path.join(download_folder, file_name)
            await file_info.download_to_drive(file_path)
            logger.info(f"Arquivo baixado para: {file_path}")
            await update.message.reply_text("Arquivo baixado. Iniciando análise...")

            try:
                audio_path = await self.tool.extract(file_path)
                transcription_path = await self.tool.transcription(audio_path)
                note_path = await self.tool.save_note(transcription_path)
                await update.message.reply_text("Nota do vídeo criada com sucesso!")

                if os.path.exists(note_path):
                    with open(note_path, 'rb') as f:
                        await update.message.reply_document(f, caption="Sua nota do vídeo está pronta!")
                else:
                    logger.warning(f"Nota final não encontrada em: {note_path}")
                    await update.message.reply_text("A nota foi criada, mas não consegui localizá-la para enviar de volta.")

            except Exception as e:
                logger.exception(f"Erro ao processar arquivo de {update.effective_user.full_name}")
                await update.message.reply_text(f"Ocorreu um erro ao processar seu arquivo: {e}")
        else:
            await update.message.reply_text("Não consegui identificar o arquivo enviado.")

    def run(self):
        logger.info("Iniciando o bot do Telegram...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    bot = LIENYXTelegramBot()
    bot.run()