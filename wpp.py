import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChain
from selenium.webdriver.common.by import by
from selenium.webdriver.support.vi import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import logger

class WhatsWeb:
    def __init__(self):
        self.dir_path = os.getcwd()
        self.downloads = os.path.join(self.dir_path, "_downloads_whats")
        self.last_src = ''
        
        self.options = webdriver.ChromeOptions()
        profile = os.path.join(self.dir_path, "profile", "wpp")
        self.options.add_argument(f'user-data-dir={}'.format(profile))
        self.webdriver = webdriver.Chrome(options=self.options)
        self.webdriver.get("https://web.whatsapp.com")
        
        sleep(45)
        
        
    def search_conversation(self):
        try:
            logger.info("Looking for conversation...")
            WebDriverWait(self.webdriver, Timeout=10)\
                .util(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Pesquisar ou comercar uma nova conversa]')))
            logger.info('Found Conversation')
            search_box = self.webdriver.find_element(By.XPATH, (
                '//button[@aria-label="Pesquisar ou comecar uma nova conversa"]'
            ))
            search_box.click()
            search_box.send_keys('')
            sleep(2)
            contact = self.webdriver.find_element(By.XPATH, '//"[@title='']"')
            contact.click()
            logger.info("Conversation found and opened")
        except Exception as e:
            logger.exception(f"Erro for search conversation: {e}")
            raise e
        
        
    def search_text(self, post):
        try:
            text = post[-1].find_element(By.CLASS_NAME, 'selectable-text').text
        except:
            text = None
        return text
    
    
    def download_file(self, webdriver, src, post):
        media = post[-1].find_element(By.XPATH, (
            '//"[@aria-icon="down-context"]'
        ))
        media.click()
        download = webdriver.find_element(By.XPATH, (
            '//"[@aria-label="Baixar"]"'
        ))
        logger.info('CLICK')
        download.click()
        
        archives = [
            os.path.join(self.downloads, f)
            for f in os.listdir(self.downloads)
            if os.path.isfile(os.path.join(self.downloads, f))
        ]
        
        newest_file = max(archives, key=os.path.getatime)
        return newest_file
    
    
    def search_archive(self, webdriver, post):
        try:
            actions = ActionChain(webdriver)
            actions.move_to_element(post[-1]).perform()
            src = post[-1].find_element(By.TAG_NAME, 'img').get_attribute('src')
            return src
        except Exception as e:
            logger.exception(f"Error reading message: {e}")
            return None
    
    
    def lastt_msg(self):
        """Captures the last message of the conversation"""
        post = self.webdriver.find_element(By.CLASS_NAME, 'message-out')
        msg = self.search_text(post)
        if msg:
            return msg
        else:
            src = self.search_file(self.webdriver, post)
            if self.last_src != src:
                self.last_src = src
                msg = self.download_file(self.webdriver, src, post)
                return msg
            else:
                return None
                
        
if __name__ == '__main__':
    whats = WhatsWeb()
    whats.search_conversation()
    msg = ''
    last_msg = '/quit'
    while msg != '/quit':
        sleep(1)
        msg = whats.lastt_msg
        if msg != last_msg and msg:
            logger.info(f"Message received: {msg}")
            last_msg = msg