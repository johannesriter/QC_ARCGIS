import os, shutil
import requests
from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def choosing_driver(input_driver):

    if input_driver == 'chrome':
        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service)
    
    elif input_driver == 'edge':
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(options=options)

    elif input_driver == 'firefox':
        driver = webdriver.Firefox()

    return driver

def check_web_access(driver, url_page, wa_portal, wa_server, uname, pwd):

    wait = WebDriverWait(driver, 60)
    driver.maximize_window()

    print('UAT Scenario for Portal')
    driver.get('{}/{}/home'.format(url_page, wa_portal))

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div/div/div[2]/div[11]/div/button')))
    driver.find_element(By.XPATH, '//*[@id="header"]/div/div/div[2]/div[11]/div/button').click()

    print('Portal landing page Response : 200')

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginTitle"]')))
    driver.find_element(By.XPATH, '//*[@id="loginTitle"]').click()
    time.sleep(10)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user_username"]')))
    driver.find_element(By.XPATH, '//*[@id="user_username"]').send_keys(uname)
    time.sleep(10)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user_password"]')))
    driver.find_element(By.XPATH, '//*[@id="user_password"]').send_keys(pwd)
    time.sleep(10)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signIn"]')))
    driver.find_element(By.XPATH, '//*[@id="signIn"]').click()

    print('Sign in page Response : 200')
    time.sleep(10)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-5"]')))
    driver.find_element(By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-5"]').click()
    
    print('Content page Response : 200')

    ### Saved line for published hosted
    # wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="create-dropdown"]')))
    # driver.find_element(By.XPATH, '//*[@id="create-dropdown"]').click()
    ### Saved line for published hosted

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-6"]')))
    driver.find_element(By.XPATH, '//*[@id="esri-header-menus-link-desktop-0-6"]').click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dijit__TemplatedMixin_0"]/div/nav/a[5]')))
    driver.find_element(By.XPATH, '//*[@id="dijit__TemplatedMixin_0"]/div/nav/a[5]').click()

    # There are bugs here
    time.sleep(10)
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/main/div/div[3]/div[1]/fieldset/ul/li[9]/button')))
    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/main/div/div[3]/div[1]/fieldset/ul/li[9]/button').click()
    time.sleep(10)

    print('Please check manual federation server')
    print('UAT Scenario for Portal is Completed')

    print('Checking login access to ArcGIS Server scenarion')
    driver.switch_to.new_window('tab')

    print('UAT Scenario for ArcGIS Server is Started')
    driver.get('{}/{}/manager'.format(url_page, wa_server))

    print('ArcGIS Server home page Response : 200')

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="navtabs"]/div[1]/ul/li[2]')))
    driver.find_element(By.XPATH, '//*[@id="navtabs"]/div[1]/ul/li[2]').click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="esri_discovery_dijit_NavigationTabs_0"]/div[3]/ul[2]/li[3]/a')))
    driver.find_element(By.XPATH, '//*[@id="esri_discovery_dijit_NavigationTabs_0"]/div[3]/ul[2]/li[3]/a').click()

    print('UAT Scenario for ArcGIS Server is Completed')
    time.sleep(10)


    time.sleep(10)
    print('UAT Scenario for Datastore is started')
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="esri_discovery_dijit_NavigationTabs_0"]/div[3]/ul[2]/li[1]/a')))
    driver.find_element(By.XPATH, '//*[@id="esri_discovery_dijit_NavigationTabs_0"]/div[3]/ul[2]/li[1]/a').click()

    time.sleep(10)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dataStoresLabel"]')))
    driver.find_element(By.XPATH, '//*[@id="dataStoresLabel"]').click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="data"]/div[3]/table/tbody/tr/td[1]/span[2]')))
    driver.find_element(By.XPATH, '//*[@id="data"]/div[3]/table/tbody/tr/td[1]/span[2]').click()
    
    print('UAT Scenario for Datastore is completed')
    time.sleep(60)

    print('All UAT Scenario is Completed')

if __name__ == "__main__":
    url = input('Please input portal url example (https://machine.domain.com): ')
    uname = input('Please input administrator username : ')
    pwd = input('Please input administrator password: ')

    web_adaptor_portal = input('Please input web adaptor portal: ')
    web_adaptor_server = input('Please input web adaptor server: ')

    input_driver = input('Please input your browser that will be used for automation [edge/chrome/firefox]: ')
    
    try:
        print('Preparing the web driver, you have choose {}'.format(input_driver))
        get_driver = choosing_driver(input_driver)
        print('Webdriver is completed')

        check_web_access(get_driver, url, web_adaptor_portal, web_adaptor_server, uname, pwd)
    except Exception as e:
        raise(e)