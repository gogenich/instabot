from selenium import webdriver
import time
import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd


def Login(login,passwod):
    """подключение к сайту, принимает логин и пароль затев осуществляет вход в аккаунт"""
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")

    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    driver.get("https://www.instagram.com/")
    time.sleep(random.randint(10, 30)/10)

    """находим поле логина и вводим логин"""
    log = driver.find_element_by_xpath("//input[@aria-label = 'Телефон, имя пользователя или эл. адрес']")
    log.send_keys(login)

    """водим пароль"""
    pas = driver.find_element_by_xpath("//input[@aria-label = 'Пароль']")
    pas.send_keys(passwod)

    """нажимаем кнопку войти"""
    but = driver.find_element_by_xpath("//div[text() = 'Войти']")
    but.click()
    time.sleep(random.randint(70, 150)/10)

    """переход на главную страничку"""
    general_list = driver.find_element_by_xpath("//div[@class= 'q9xVd']")
    general_list.click()
    time.sleep(random.randint(10, 30)/10)
    '''отключили всплывающее окно'''
    driver.find_element_by_xpath("//button[text() = 'Не сейчас']").click()
    return driver

def collect_post(teg, n):
    """функция собирающая ссылки на посты с тегами"""
    rezult = []
    sessia.get(f'https://www.instagram.com/explore/tags/{teg}/')
    time.sleep(random.randint(70, 130) / 10)
    while len(rezult) < n:
        links = sessia.find_elements_by_xpath("//div[contains(@class, 'v1Nh3 kIKUG')]/a")
        for i in range(len(links)):
            link = links[i].get_attribute('href')
            rezult.append(link)
        '''скролим вниз'''
        actions = ActionChains(sessia)
        actions.move_to_element(links[-1]).key_down(Keys.ENTER)
        actions.perform()
        time.sleep(random.randint(10, 30) / 10)
        rezult = list(set(rezult))
        print(f'собрано {len(rezult)} ссылок')
    '''переходим на главную страничку'''
    sessia.get("https://www.instagram.com/")
    return rezult

def collect_users(user, n):
    """функция собирающая ссылки друзей пользователя"""
    sessia.get(f'https://www.instagram.com/{user}/followers/')
    time.sleep(random.randint(10, 30) / 10)
    sessia.find_element_by_xpath("//a[text() = ' подписчиков']").click()
    time.sleep(random.randint(30, 60) / 10)
    users_links = []
    while len(users_links) < n:
        users = sessia.find_elements_by_xpath("//span[@class = 'Jv7Aj mArmR MqpiF  ']/a")
        for user in users:
            users_links.append(user.get_attribute('href'))

        actions = ActionChains(sessia)
        actions.move_to_element(users[-1])
        actions.perform()
        users[-1].send_keys(Keys.PAGE_DOWN)
        users_links = list(set(users_links))
        print(f'собрано {len(users_links)} пользователей')
        time.sleep(random.randint(10, 30) / 10)
    return users_links

def like(tegi):
    """функция которая принимает список ссылок на посты, переходит по ним и лайкает"""
    for teg in tegi:
        sessia.get(teg)
        try:
            sessia.find_element_by_xpath("//span[@class = 'fr66n']").click()
            print(f'лайкнул {teg}')
        except Exception:
            print(f'ссылка {teg} скорее всего удалена')
        time.sleep(random.randint(20, 70) / 10)

def comment(tegi):
    """функция которая принимает список ссылок на посты, переходит по ним и комментирует"""
    fail = open('comment_data', 'r')
    com = [el.strip() for el in fail]
    for teg in tegi:
        sessia.get(teg)
        i = random.randint(0, len(com))
        try:
            sessia.find_element_by_xpath("//span[@class = '_15y0l']").click()
            time.sleep(random.randint(10, 30) / 10)
            actions = ActionChains(sessia)
            actions.send_keys(com[i])
            actions.perform()
            sessia.find_element_by_xpath("//button[@type = 'submit']").click()
            print(f'прокоментировал {teg}')
        except Exception:
            print(f'ссылка {teg} скорее всего удалена')
        time.sleep(random.randint(100, 160) / 10)

"""пример работы бота"""
log = '******'
pas = '******'

sessia = Login(log, pas)
time.sleep(5)

users = collect_users('misik_29', 10)
tegi = collect_post('море', 10)
like(tegi[:8])
comment(tegi[8:])
print(f'ссылки постов {tegi}')
print(f'ссылки пользователей {users}')

# start = time.time()
#
# sessia = Login(log, pas)
# time.sleep(5)
# tegi = collect_post('море', 10)
# like(tegi[:8])

# h = 0
# start_like = 0
# finish_like = random.randint(5, 5)
# while h < 20:
#     fin = time.time()
#     if fin - start > 3600:
#         print('\nпошел новый час:')
#         like(tegi[start_like:finish_like])
#         start_like = finish_like
#         finish_like = start_like + random.randint(1, 5)
#         comment(tegi[start_like:finish_like])
#         start_like = finish_like
#         finish_like = start_like + random.randint(15, 30)
#         h = h + 1
#         start = time.time()
#     time.sleep(random.randint(300, 600))
# print(finish_like)
# print('end')


