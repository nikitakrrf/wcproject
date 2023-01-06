import random
import time

import requests as requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Post_form(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:/Users/psiap/AppData/Local/Google/Chrome/User Data/Default")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.__driver = webdriver.Chrome(executable_path=r'chromedriver.exe', chrome_options=options)

    def get_url_start(self):
        url = 'https://web.whatsapp.com/'
        self.__driver.get(url)
        self.__driver.maximize_window()
        self.__driver.implicitly_wait(3)
        WebDriverWait(self.__driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[3]/header/div[1]/div/img'))
        )
        #

    def _one_page_url(self,number):
        self.__driver.get(f'https://web.whatsapp.com/send/?phone={number}')

    def _two_page_check_online(self):
        try:
            time.sleep(3)
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span'))
            )
            time.sleep(3)
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span'))
            )
            result = element.text
            if 'данные контакта' in result:
                result = f'Off {element.text}'
            elif 'был' in result:
                result = f'Off {element.text}'
            else:
                result = f'On {element.text}'
        except:
            result = 'Off'
        return result

    def __start__(self):
        self.get_url_start()
        response = requests.get('http://127.0.0.1:8000/api/v1/number').json()
        for _num in response['users']:
            if _num['is_parser']:
                self._one_page_url(number=_num)
                result = self._two_page_check_online()
                if result == 'Off':
                    requests.put('http://127.0.0.1:8000/api/v1/number', data={'user_id': _num['user_id'],
                                                                              'number': _num['number'],
                                                                              'is_parser': True,
                                                                              'is_online': False,
                                                                              'last_online': result})
                else:
                    requests.put('http://127.0.0.1:8000/api/v1/number', data={'user_id': _num['user_id'],
                                                                               'number': _num['number'],
                                                                               'is_parser': True,
                                                                               'is_online': True,
                                                                               'last_online': result})

if __name__ == '__main__':
    while True:
        test_class = Post_form()
        test_class.__start__()


    #requests.post('http://127.0.0.1:8000/api/v1/number', data={'user_id': 'nikita_0001',
    #                                                            'number': '380713891427',
     #                                                           'is_parser': True,
     #                                                           'is_online': False})



