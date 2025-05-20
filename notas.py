import os
from langchain_openai import ChatOpenAI
from dotenv import load_dontenv
from logger import logger

load_dontenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

class Notas:
    def create_tags(text):
        """"""
        logger.info('Creating tags...')
        tags = llm.invoke(
            f'Crie ate 10 tags referentes a este texto: \n{text}\n'
            f'Voce deve responder apenas as tags, sem nenhum comentario, nem numeracao'
            f'as tags devem estar alinhadas em uma unica linha, separadas por um espaco'
            f'Eles devem ser relacionadas apenas ao conteudo do texto'
            f'por exemplo, um que fale sobre filosofia pode ter a tag #filosofia'
            f'outro exemplo, um texto que fale sobre treino de academia pode ter as tags #fitness #health'
            f'todas a tags devem ter # na frente, por exemplo: #exemplo'
            )
        return tags.content
    
    
    def create_short_summary(text):
        """creates a short summary of up to 20 words of the transcript"""
        logger.info('Creating short summary...')
        short_summary = llm.invoke(
            f'Crie um resumo do texto em 20 palavras: \n{text}'
            )
        return short_summary.content
    
    
    def create_detailed_summary(text):
        """Creates a detailed transition summary"""
        logger.info('Creating detailed summary...')
        detailed_summary = llm.invoke(
            f'Resuma detalhadamente o texto: \n{text}\n'
            f'mantendo  todas as informacoes importantes de forma estruturada'
            f'o Resumo deve conter todas as informacoes para que uma pessoa que nao leu o texto original possa entender por completo o conteudo'
            )
        return detailed_summary.content
    
    
    def create_bullet_point(text):
        """Creates a bullet point based on the transcript"""
        logger.info('Creating bullet point...')
        bullet_point = llm.invoke(
            f'Liste um bullet point as principais ideias referentes ao texto: \n{text}'
            )
        return bullet_point.content
    
    
    def format_note(tags, short_summary, detailed_summary, bullet_point):
        """Formats the texts in a single note with title, #tags, summaries"""
        logger.info('Formatting text...')
        final_text = (
            f'{tags}\n\n'
            f'# Resumo do Video\n\n#'
            f'## Resumo Curto\n{short_summary}\n\n'
            f'## Resumo Detalhado\n{detailed_summary}\n\n'
            f'## Bullet Points\n{bullet_point}\n\n'
            )
        return final_text
    
    
    def save_note(transcription_path):
        """Saves the text in a text file in the _notes directory"""
        logger.info('Creating note text')
        
        transcription_path = transcription_path.replace("'", "")
        logger.debug(f'transcription_path {transcription_path}')
        
        with open(transcription_path, 'rb') as file:
            transcription = file.read()
            tags = Notes.create_tags(transcription)
            short_summary = Notes.create_short_summary(transcription)
            detailed_summary = Notes.detailed_summary(transcription)
            bullet_point = Notes.create_bullet_point(transcription)
            nota = Notes.format_note(tags, short_summary, detailed_summary, bullet_point)
            logger.info('Create note\n\n')
            
        output_path = os.path.dirname(transcription_path)
        output_path = output_path.replace('transcription', 'notes')
        
        base_name = os.path.splitext(os.path.basename(transcription_path))[0]
        summary_path = f'{output_path}/{base_name}.md'
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            logger.info(f"Creating folder '_notes' in: {output_path}")
            
        with open(summary_path, 'w') as f:
            f.write(nota)
        logger.info(f'save note in: {summary_path}')
        
        
if __name__ == '__main__':
    transcription_path = ''
    Notes.save_note(transcription_path)