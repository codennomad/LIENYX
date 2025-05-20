import base64
from io import BytesIO
from PIL import Image
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from logger import logger

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

class ProcessImage:
    def openai_analysis(self, image_peth):
        """
        Analyzes image, and describes its content in detail
        if it has texts, transcribe in markdown format
        """
        pil_image = Image.open(img_path)
        buffered = BytesIO()
        pil_image.save(buffered, format='JPEG')
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        input = [
            [HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": """
                        Analise a imagem, e descreva detalhamente seu conteudo.Caso ela possua textos, transcreva-os em formato markdown.
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_str}"
                        }
                    }
                ]
            )],
        ]
        image_analysis = llm.invoke(input[0])
        return image_analysis

if __name__ == '__main__':
    img = ProcessImage()
    img_path = ''
    image_analysis = img.openai_analysis(img_path).content
    logger.info(image_analysis)