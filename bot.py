from time import sleep
from datetime import datetime
from random import randint

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class InstaBot:

    def __init__(self, login, password):

        self.login = login
        self.password = password

        """создание драйвера"""
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)

    def input_account(self):

        """подключение к сайту, принимает логин и пароль затев осуществляет вход в аккаунт"""

        self.driver.get("https://www.instagram.com/")
        sleep(randint(10, 30)/10)

        """находим поле логина и вводим логин"""
        log = self.driver.find_element_by_xpath("//input[@aria-label = 'Телефон, имя пользователя или эл. адрес']")
        log.send_keys(self.login)

        """водим пароль"""
        pas = self.driver.find_element_by_xpath("//input[@aria-label = 'Пароль']")
        pas.send_keys(self.password)

        """нажимаем кнопку войти"""
        but = self.driver.find_element_by_xpath("//div[text() = 'Войти']")
        but.click()
        sleep(randint(70, 150)/10)

        """переход на главную страничку"""
        general_list = self.driver.find_element_by_xpath("//div[@class= 'q9xVd']")
        general_list.click()
        sleep(randint(10, 30)/10)
        '''отключили всплывающее окно'''
        self.driver.find_element_by_xpath("//button[text() = 'Не сейчас']").click()

        with open('logi.txt', 'a') as f:
            f.writelines(f'bot input_account {datetime.now()}\n')

    def collect_post(self, teg, n):

        """функция собирающая ссылки на посты с тегами"""

        result = []

        self.driver.get(f'https://www.instagram.com/explore/tags/{teg}/')
        sleep(randint(70, 130) / 10)
        while len(result) < n:
            links = self.driver.find_elements_by_xpath("//div[contains(@class, 'v1Nh3 kIKUG')]/a")
            for i in range(len(links)):
                link = links[i].get_attribute('href')
                result.append(link)
            '''скролим вниз'''
            actions = ActionChains(self.driver)
            actions.move_to_element(links[-1]).key_down(Keys.ENTER)
            actions.perform()
            sleep(randint(10, 30) / 10)
            result = list(set(result))
            '''формируем отчет'''
            with open('logi.txt', 'a') as f:
                f.writelines(f'collect {len(result)} links {datetime.now()}\n')

        '''переходим на главную страничку'''
        self.driver.get("https://www.instagram.com/")
        return result

    def collect_users(self, user, n):
        """функция собирающая ссылки друзей пользователя"""
        self.driver.get(f'https://www.instagram.com/{user}/followers/')
        sleep(randint(10, 30) / 10)
        self.driver.find_element_by_xpath("//a[text() = ' подписчиков']").click()
        sleep(randint(30, 60) / 10)
        users_links = []
        while len(users_links) < n:
            users = self.driver.find_elements_by_xpath("//span[@class = 'Jv7Aj mArmR MqpiF  ']/a")
            for user in users:
                users_links.append(user.get_attribute('href'))

            actions = ActionChains(self.driver)
            actions.move_to_element(users[-1])
            actions.perform()
            users[-1].send_keys(Keys.PAGE_DOWN)
            users_links = list(set(users_links))

            '''формируем отчет'''
            with open('logi.txt', 'a') as f:
                f.writelines(f'collect {len(users_links)} users {datetime.now()}\n')

            sleep(randint(10, 30) / 10)
        return users_links

    def like(self, tegi):

        """функция которая принимает список ссылок на посты, переходит по ним и лайкает"""
        for teg in tegi:
            self.driver.get(teg)
            try:
                self.driver.find_element_by_xpath("//span[@class = 'fr66n']").click()
                with open('logi.txt', 'a') as f:
                    f.writelines(f'put a like {teg} {datetime.now()}\n')

            except Exception:

                with open('logi.txt', 'a') as f:
                    f.writelines(f'link {teg} delete')

            sleep(randint(20, 70) / 10)

    def comment(self, tegi):
        """функция которая принимает список ссылок на посты, переходит по ним и комментирует"""
        fail = open('comment_data', 'r')
        com = [el.strip() for el in fail]
        for teg in tegi:
            self.driver.get(teg)
            i = randint(0, len(com))
            try:
                self.driver.find_element_by_xpath("//span[@class = '_15y0l']").click()
                sleep(randint(10, 30) / 10)
                actions = ActionChains(self.driver)
                actions.send_keys(com[i])
                actions.perform()
                self.driver.find_element_by_xpath("//button[@type = 'submit']").click()
                with open('logi.txt', 'a') as f:
                    f.writelines(f'comment {teg} {datetime.now()}\n')
            except Exception:

                with open('logi.txt', 'a') as f:
                    f.writelines(f'link {teg} delete')
            sleep(randint(100, 160) / 10)
    def exit_account(self):
        self.driver.quit()


"""пример работы бота"""
now = datetime.now()

log = '*****'
pas = '*****'

account = InstaBot(log, pas)
account.input_account()

sleep(5)

hashteg = 'зима'

random_post = [randint(5, 15)for el in range(randint(5, 15))]
posts = account.collect_post(hashteg, sum(random_post))
start = 0

for el in random_post:
    finish = el + start
    account.like(posts[start:finish])
    start = el
    sleep(randint(600, 1200))

finish_time = f'finish_time = {datetime.now()}'

with open(f'report_{now}.txt', 'a') as f:
    f.writelines(f'bot start {now}\n')
    f.writelines(f'bot finish {datetime.now()}\n')
    f.writelines(f'bot use hashteg {hashteg}\n')
    f.writelines(f'quantity posts = {len(posts)}\n')
    for el in posts:
        f.writelines(f'{el}\n')

account.exit_account()



