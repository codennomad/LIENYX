from time import sleep
from langchain_agents import(
    AgentExcutor,
    create_tool_calling_agent
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tools import LIENYXTools
from wpp import WhatsWeb
from logger import logger

load_dotenv()

class LIENYX:
    def __init__(self):
        self.llm = ChatOpenAI(model='gpt-4o-mini')
        self.tool = LIENYXTools()
        self.whats = WhatsWeb()
       
        
    def create_agent(self):
        tools = [
            Tool(name="download_video", func=LIENYXTools.download_video, description="Baixa video do youtube e"),
            Tool(name="extract", func=LIENYXTools.extract, description="Extrai o audio de um arquivo MP4"),
            Tool(name="ProcessImage", func=LIENYXTools.ProcessImage, description="Analisa o image_path e retorna uma"),
            Tool(name="transcription", func=LIENYXTools.transcription, description="Transcrive um arquivo de audio e salva"),
            Tool(name="save_note", func=LIENYXTools.save_note, description="Salva o texto em um arquivo de texto no diret"),
        ]
        llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    Seu nome e LIENYX um assistente especializado em ajudar os usuarios a criar notas detalhadas e completas.
                    Voce auxilia extraindo as informacoes principais, organizando-as em pontos estruturados e garantindo que as notas finais sejam abrangentes.
                    Sempre resuma as informacoes de maneira clara e concisa.
                    Mantanha o controle dos resultados das ferramentas e incorpore-os as notas conforme necessario.
                    O resultado final deve estar em portugues Brasileiro e formatado em Markdown.
                    """
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        agent = create_tool_calling_agent(
            llm=llm,
            tools=tools,
            prompt=prompt
        )
        return agent, tools
    
    
    def process_mensagem(self, msg, agent, tools):
        """"""
        agent_executor = AgentExecutor.from_agent_add_tools(
            agent = agent,
            tools = tools,
            verbose = True,
        )
        executor_prompt = {"input": # falta aqui}

        result = agent_executor.invoke(executor_prompt)
        return result

if __name__ == '__main__':
    bot = LIENYX()
    bot.whats.search_conversation()
    msg = ''
    agente, tools = bot.creatre_agent()
    last_msg = '/quit'
    while msg != '/quit':
        sleep(1)
        msg = bot.whats.lastt_msg()
        if msg != last_msg and msg:
            logger.info(f"Message Received: {msg}")
            last_msg = msg
            try:
                result = bot.process_message(msg, agente, tools)
                logger.info(f"Result: {result}")
            except Exception as e:
                logger.exception(e)