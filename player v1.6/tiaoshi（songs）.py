from selenium import webdriver
import time


def lyrics_get(driver, id_, id_name):
    driver.get('https://music.163.com/#/song?id={}'.format(id_))
    time.sleep(2)
    print(driver.title, '-------------')

    driver.switch_to.frame('g_iframe')
    req = driver.find_elements_by_id('lyric-content')

    driver.execute_script("window.scrollBy(0, 500)")  # "window.scrollBy(0,1200)"

    click_extend = driver.find_element_by_id('flag_ctrl').find_element_by_tag_name('i')
    click_extend.click()

    print(req[0].text)
    with open('lyrics/{}'.format(id_name), 'w', encoding='utf-8') as f:
        f.write(req[0].text)

if __name__ == "__main__":

    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=option)

    lyrics_get(driver, '1442825489', '是首俗歌 (Live) - (我是唱作人2第2期)')
