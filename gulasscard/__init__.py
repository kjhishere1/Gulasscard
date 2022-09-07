from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException

from time import sleep

URLs = {
    "Main": "https://www.classcard.net",
    "Login": "https://www.classcard.net/Login",
}

def get_driver(URL, waitby=(By.TAG_NAME, "body"), timeout=3, options=None):
    if options == None:
        options = webdriver.ChromeOptions()
        #options.add_experimental_option("detach", True)
        options.binary_location = r"C:\Users\super\Downloads\gc\chrome\App\Chrome-bin\chrome.exe"

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException:
        raise ValueError()
    driver.get(URL)

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(waitby)
    )
    return driver

def Login(USERNAME: str, PASSWORD: str, driver=None):
    if driver == None:
        driver = get_driver(URLs['Login'], (By.ID, "loginForm"))

    assert "클래스카드" in driver.title

    loginForm = driver.find_element(By.ID, "loginForm")
    idForm = loginForm.find_element(By.ID, 'login_id')
    pwdForm = loginForm.find_element(By.ID, 'login_pwd')
    loginButton = loginForm.find_element(By.TAG_NAME, 'button')

    idForm.send_keys(USERNAME)
    pwdForm.send_keys(PASSWORD)
    loginButton.click()

    sleep(.3)

    try:
        idFail = loginForm.find_element(By.ID, 'login_fail_id')
        pwdFail = loginForm.find_element(By.ID, 'login_fail_pwd')

        for fail in [idFail, pwdFail]:
            if 'hidden' not in fail.get_attribute('class').split(' '):
                return None
    except StaleElementReferenceException:
        return driver


def Set(URL, driver=None):
    if driver == None:
        driver = get_driver(URL)
    
    driver.get(URL)

    dropdowns = driver.find_elements(By.CLASS_NAME, "dropdown")
    for dropdown in dropdowns:
        if dropdown.get_attribute("innerText").endswith('▼'):
            dropdown.click()
            dropdown_menu = dropdown.find_element(By.CLASS_NAME, 'dropdown-menu')
            dropdown_menu.find_elements(By.TAG_NAME, 'li')[0].click()
            return driver
    return None

def Get(URL=None, driver=None):
    if driver == None:
        driver = get_driver(URL)

    word_dict = {}
    word_set = driver.find_element(By.CSS_SELECTOR, '.tab-pane > .word-set')
    word_cards = word_set.find_elements(By.CLASS_NAME, "flip-card")
    for card in word_cards:
        details = card.get_attribute('innerText').split('\n')
        word = details[0].strip()
        lines = []

        for line in details[1:]:
            if line.find(word) == -1:
                lines.append(line.strip())
        lines.append(' '.join(lines))
        word_dict[word] = lines
    return driver, word_dict

def Memorize(URL=None, driver=None):
    if driver == None:
        driver = get_driver(URL)
    
    driver.get(URL)
    buttons = driver.find_elements(By.CLASS_NAME, "btn")
    for btn in buttons:
        if btn.get_attribute('innerText') == "암기 학습 시작 (전체구간)":
            btn.click()
            break

    sleep(1.5)

    known = lambda: int(driver.find_element(By.CLASS_NAME, "known_count").get_attribute('innerText'))
    total = int(driver.find_element(By.CLASS_NAME, "total_count").get_attribute('innerText'))

    study = driver.find_element(By.CLASS_NAME, 'study-bottom')
    next = driver.find_element(By.CLASS_NAME, 'btnNextCard')

    while known() < total:
        study.find_element(By.CLASS_NAME, 'btn-down-cover-box').click()
        sleep(.3)
        study.find_element(By.CLASS_NAME, 'btn-short-change-card').click()
        next.click()
        sleep(.3)
    

def Recall(URL, get):
    driver, words = get
    driver.get(URL)
    buttons = driver.find_elements(By.CLASS_NAME, "btn")
    for btn in buttons:
        if btn.get_attribute('innerText') == "리콜 학습 시작 (전체구간)":
            btn.click()
            break

    sleep(2.5)

    known = lambda: int(driver.find_element(By.CLASS_NAME, "known_count").get_attribute('innerText'))
    total = int(driver.find_element(By.CLASS_NAME, "total_count").get_attribute('innerText'))

    while known() < total:
        sleep(2.6)
        card = driver.find_element(By.CSS_SELECTOR, '.CardItem.current.showing')
        word = card.find_element(By.CSS_SELECTOR, ".card-top .text-normal > .normal-body").get_attribute('innerText')
        quests = card.find_elements(By.CSS_SELECTOR, '.card-quest-front .card-quest-list > div')

        word_sel = [quest.get_attribute('innerText').strip() for quest in quests]
        for idx, kor in enumerate(word_sel):
            if kor in words[word]:
                try:
                    quests[idx].click()
                except ElementClickInterceptedException:
                    return True
                break



if __name__ == '__main__':
    if type((driver := Login('username', 'password'))) is not str:
        if (driver := Set('https://www.classcard.net/set/9434311/728808', driver=driver)) is not None:
            Recall('https://www.classcard.net/Recall/9434311/6000/728808', Get(driver=driver))
            #Memorize('https://www.classcard.net/Memorize/9434311/6000/728808', driver=driver)