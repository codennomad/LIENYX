import base64
import asyncio
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os 
from lienyx.logger import logger 
load_dotenv()

# Crie um ThreadPoolExecutor para executar operações de bloqueio
executor = ThreadPoolExecutor()

# O LLM é inicializado uma vez
# Certifique-se de que OPENROUTER_API_KEY esteja no seu .env
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model='gpt-4o-mini', 
    temperature=0
)

class ProcessImage:
    async def openai_analysis(self, image_path):
        """
        Analisa a imagem e descreve seu conteúdo em detalhes assincronamente.
        Caso tenha texto, transcreve em formato Markdown.
        """
        try:
            logger.info(f"Analisando imagem: {image_path}")
            
            # Operação de leitura e codificação de imagem em um thread separado
            loop = asyncio.get_running_loop()
            img_str = await loop.run_in_executor(executor, self._sync_process_image, image_path)

            input_message = [
                HumanMessage(
                    content=[
                        {"type": "text", "text": """
                        Analise a imagem, e descreva detalhadamente seu conteudo. Caso ela possua textos, transcreva-os em formato markdown.
                        """},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
                    ]
                )
            ]
            
            # Usar ainvoke para chamar o LLM assincronamente
            image_analysis = await llm.ainvoke(input_message[0])
            logger.info("Análise da imagem concluída com sucesso")
            return image_analysis.content 
        except Exception as e:
            logger.exception("Erro ao analisar imagem")
            raise e

    def _sync_process_image(self, image_path):
        """Parte síncrona do processamento de imagem a ser executada no executor."""
        pil_image = Image.open(image_path)
        buffered = BytesIO()
        pil_image.save(buffered, format='JPEG')
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

if __name__ == '__main__':
    async def test_image_analysis():
        img = ProcessImage()
        # Substituir com caminho real da imagem para teste
        img_path = 'caminho/para/sua/imagem.jpg' 
        if os.path.exists(img_path):
            try:
                image_analysis_content = await img.openai_analysis(img_path)
                print(f"Análise da imagem:\n{image_analysis_content}")
            except Exception as e:
                print(f"Erro no teste de análise de imagem: {e}")
        else:
            print("Caminho da imagem de teste não encontrado. Por favor, atualize 'img_path'.")

    # Para rodar o teste
    # asyncio.run(test_image_analysis())
    pass # Deixe como pass por enquanto para não interferir com main.py