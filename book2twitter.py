import pdfplumber as pp
import random
import time
from selenium import webdriver

def log_in(username, password):

    browser = webdriver.Firefox()
    browser.implicitly_wait(5)

    browser.get('https://twitter.com/login')
    username_input = browser.find_element_by_css_selector('input[name="session[username_or_email]"]')
    password_input = browser.find_element_by_css_selector('input[name="session[password]"]')

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_link = browser.find_element_by_css_selector('div[data-testid="LoginForm_Login_Button"]')
    login_link.click()

    return browser

def post_sentence(sentence, browser):
    tweet_window = browser.find_element_by_css_selector('div[class="DraftEditor-root"]')
    tweet_window.click()

    text_window = browser.find_element_by_css_selector('div[class="notranslate public-DraftEditor-content"]')
    text_window.send_keys(sentence)

    tweet_button = browser.find_element_by_css_selector('div[data-testid="tweetButtonInline"]')
    tweet_button.click()

def generate_sentence(pdf):
    number = random.randint(0, len(pdf.pages) - 1)
    page = pdf.pages[number]
    text = page.extract_text()

    start = random.randint(0, len(text) - 1)
    ini = start
    cursor = text[ini]
    sentence = text[ini]

    while cursor != '.':

        ini += 1
        cursor = text[ini]
        sentence += cursor
        if len(sentence) > 280:
            break

    ini = start - 1
    cursor = text[ini]

    while cursor != '.':
        cursor = text[ini]
        sentence = cursor + sentence
        ini -= 1
        if len(sentence) > 280:
            break

    sentence = sentence[2:]

    return sentence

if __name__ == '__main__':

    with pp.open("path/book.pdf") as pdf:

        browser = log_in('user', 'password')

        while True:

            sentence = generate_sentence(pdf)

            while sentence[-1] != '.':
                sentence = generate_sentence(pdf)

            print(sentence)

            post_sentence(sentence, browser)

            time.sleep(8*60*60)

