from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import time
import re
import os

Account = 'YOUR_ACCOUNT'
Password = 'YOUR_PASSWORD'

driver = webdriver.Chrome('THE_ABSOLUTE_PATH_OF_CHROMEDRIVER_THAT_YOU_JUST_INSTALLED')

suffix = {'cpp': 'cpp', 'cplusplus': 'cpp', 'c++': 'cpp', 'c': 'c',
          'java': 'java', 'python': 'py', 'py': 'py', 'c#': 'cs',
          'csharp': 'cs', 'javascript': 'js', 'js': 'js', 'ruby': 'rb',
          'rb': 'rb', 'go': 'go', 'golang': 'go', 'swift': 'swift'}

def save_ac_code(ac_list):
    
    for ac in reversed(ac_list):
        url = ac['url']

        driver.get(url);
        time.sleep(5)

        htmlObj = driver.page_source
        soup = BeautifulSoup(htmlObj, 'html.parser')
        ac_submission = soup.find_all('strong', text='Accepted')
        
        url_base = 'https://leetcode.com'
        driver.get(url_base + ac_submission[0].parent['href'])
        htmlObj = driver.page_source
        soup = BeautifulSoup(htmlObj, 'html.parser')
        code = soup.find_all('div', attrs={'class':'ace_line'})
        script = soup.find('script', text=re.compile('submissionCode:'))
        code = re.findall("submissionCode:\s*'(.+)'",script.string)[0].decode('unicode-escape')
        suff = suffix_conversion(re.findall("getLangDisplay:\s*'(.+)'",script.string)[0])
    
        id = str(ac['id'])
        if len(id) < 2:
            id = "00" + id
        elif len(id) < 3:
            id = "0" + id

        directory = id + '. ' + ac['title']
        print (directory + " saved")

        if not os.path.exists(directory):
            os.makedirs(directory)
    
        completeName = os.path.join(directory, '{}.{}'.format('Solution', suff)) 
        file = open(completeName, 'w')
        file.write(code)
        file.close()

def get_ac_problem_list():
    ac_list = []
    url = 'https://leetcode.com/api/problems/algorithms/'
    
    driver.get(url);
    pageSource = driver.page_source
    jsonObj = json.loads(driver.find_element_by_tag_name('body').text)
    
    for ac in jsonObj['stat_status_pairs']:
        if ac['status'] == 'ac':
           
            url = 'https://leetcode.com/problems/' + ac['stat']['question__title_slug'] + '/submissions'
            
            ac_info = {
                "id" : ac['stat']['question_id'],
                "title" : ac['stat']['question__title'],
                "url" : url
                }
            ac_list.append(ac_info)
    
    return ac_list


def login():
    login_url = 'https://leetcode.com/accounts/login/'

    if Account and Password:
        driver.get(login_url)

        username = driver.find_element_by_id("id_login")
        password = driver.find_element_by_id("id_password")
        
        username.send_keys(Account)
        password.send_keys(Password)

        driver.find_element_by_name("signin_btn").click()

        delay = 5 # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'home-app')))
            print "Page is ready!"
        except TimeoutException:
            print "Loading took too much time!"
        
def suffix_conversion(suff='cpp'):
    if suff in suffix:
        return suffix[suff]

if __name__ == '__main__':
    login()
    ac_list = get_ac_problem_list()
    save_ac_code(ac_list)
    
    driver.quit()


    