from pickle import dump
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def main():
    driver = webdriver.Firefox()
    driver.get('https://www.deviantart.com/users/login')
    
    try:
        username_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id="username"]')))
    except Exception as e:
        print ("Error! Cookies not updated")
        print (e)
        driver.quit()
        return
    
    username_box = driver.find_element_by_xpath('//input[@id="username"]')
    password_box = driver.find_element_by_xpath('//input[@id="password"]')
    remember_box = driver.find_element_by_xpath('//input[@id="remember"]/..')
    login_button = driver.find_element_by_xpath('//button[@id="loginbutton"]')
    
    username_box.send_keys('Aromidas')
    password_box.send_keys('cleenock')
    remember_box.click()
    login_button.click()
    
    sleep(5)
    
    cookies = driver.get_cookies()
    with open('cookies.pkl', 'wb') as f:
        dump(cookies, f)

    print ('OK Cookies updated successfully!')
    driver.quit()

main()
