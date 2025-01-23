from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

import skills_values
import skills_paths
import desired_skills
import user
import re

print('skills', skills_values)

options = webdriver.ChromeOptions()
#options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options)
driver.get("http://www.sokker.org")

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section[1]/div[2]/div[2]/div[2]/div[1]/div/div[2]/a/span/span'))).click()

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user-name"]'))).send_keys(user.user)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/div[2]/div/div/div/div[5]/form/div[2]/label/span[2]/div/div[1]/input'))).send_keys(user.password)

driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/div[2]/div/div/div/div[5]/form/div[3]/div[1]/button').click()


WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/div[2]/div/div[1]/div/div[1]/a/span/span')))
driver.get('https://sokker.org/transfers')

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="body-transfers"]/main/div/div[2]/div[2]/div[1]/div')))


for key, value in skills_values.skills_values.items():
    if value != '':
        print(key, value, skills_paths.skills_paths[key])
        element = driver.find_element(By.XPATH, skills_paths.skills_paths[key])
        if element.tag_name == 'select':
            select = Select(element)
            select.select_by_value(value)
        else:
            element.send_keys(value)



driver.find_element(By.XPATH, '//*[@id="body-transfers"]/main/div/div[2]/div[2]/div[2]/form/div[6]/div[2]/div/div/button[1]').click()

f = open("players.txt", 'a')


while True:
    tl_players = driver.find_elements(By.XPATH, '//*[@id="body-transferSearch"]/main/div/div[2]/div[2]/div[2]/div')



    for player in tl_players:
        playerText = player.find_element(By.XPATH, './div/div[2]/div').text
        href = player.find_element(By.XPATH, './div/div[2]/div/a').get_attribute('href')
        info = playerText.replace('\n', '').replace(', age ', ',').split(',')
        name = info[0]
        age = info[1]
        
        player_skills = {
            "staminia": int(re.findall(r'\d+',player.find_element(By.XPATH, './div/div[4]/table/tbody/tr[1]/td[1]/strong/span').text)[0]),
            "keeper" : int(re.findall(r'\d+',player.find_element(By.XPATH, './div/div[4]/table/tbody/tr[1]/td[2]/strong/span').text)[0]),
            "pace" :int(re.findall(r'\d+',player.find_element(By.XPATH, './div/div[4]/table/tbody/tr[2]/td[1]/strong/span').text)[0]),
            "defender" : int(re.findall(r'\d+',player.find_element(By.XPATH, './div/div[4]/table/tbody/tr[2]/td[2]/strong/span').text)[0]),
            "technique" : int(re.findall(r'\d+',player.find_element(By.XPATH, './div/div[4]/table/tbody/tr[3]/td[1]/strong/span').text)[0]),
            "playmaker" : int(re.findall(r'\d+',player.find_element(By.XPATH, './div/div[4]/table/tbody/tr[3]/td[2]/strong/span').text)[0]),
            "passing" : int(re.findall(r'\d+',player.find_element(By.XPATH, './div/div[4]/table/tbody/tr[4]/td[1]/strong/span').text)[0]),
            "striker" : int(re.findall(r'\d+',player.find_element(By.XPATH, './div/div[4]/table/tbody/tr[4]/td[2]/strong/span').text)[0])
        }


        desired_sum = 0

        for value in desired_skills.keys:
            desired_sum += player_skills[value]

        if desired_skills.threshold == 0 or desired_sum >= desired_skills.threshold:
            f.write( str(player_skills["staminia"]) + " "+ str(player_skills["pace"])+ " "  + str(player_skills["technique"])+ " "  + str(player_skills["passing"])  + " "  + str(player_skills["keeper"])  + " "  + str(player_skills["defender"])  + " "  + str(player_skills["playmaker"])  + " " + str(player_skills["striker"])  + " " + "s-" +str(desired_sum) + " " + "total-" + str(player_skills["staminia"]  + player_skills["pace"]  +  player_skills["technique"]  + player_skills["passing"]+ player_skills["keeper"] + player_skills["defender"] + player_skills["playmaker"] + player_skills["striker"]) + " " + href + " " +  " " + age  + " "+ name  + " "  +"\n")

    try:
        nextButton = driver.find_element(By.XPATH, '//*[@id="body-transferSearch"]/main/div/div[2]/div[2]/div[3]/div[1]/div/span/a[contains(text(), "»")]').click()
    except NoSuchElementException:
        break



