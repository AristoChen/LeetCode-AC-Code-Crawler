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

Account = "YOUR_ACCOUNT"
Password = "YOUR_PASSWORD"
directory = "THE_ABSOLUTE_PATH_THAT_YOU_WANT_TO_SAVE_FILES"
driver = webdriver.Chrome("THE_ABSOLUTE_PATH_OF_CHROMEDRIVER_THAT_YOU_JUST_INSTALLED")

suffix = {"cpp": "cpp", "cplusplus": "cpp", "c++": "cpp", "c": "c",
          "java": "java", "python": "py", "py": "py", "c#": "cs",
          "csharp": "cs", "javascript": "js", "js": "js", "ruby": "rb",
          "rb": "rb", "go": "go", "golang": "go", "swift": "swift"}

def save_ac_code(ac_list):
    print("Do you want to over write all files if they exists? yes/no")
    overWrite = raw_input()
    
    while overWrite.lower() != "yes" and overWrite.lower() != "no":
        print("Error:Please type 'yes' or 'no'")
        print("Do you want to over write all files if they exists? yes/no")
        overWrite = raw_input()

    for ac in reversed(ac_list):

        url = ac["url"]
        driver.get(url);

        #htmlObj = driver.page_source
        soup = BeautifulSoup(driver.page_source, "html.parser")
        ac_submission = soup.find_all("strong", text="Accepted")
        
        while len(ac_submission) == 0:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ac_submission = soup.find_all("strong", text="Accepted")
        
        driver.get("https://leetcode.com" + ac_submission[0].parent["href"])
        soup = BeautifulSoup(driver.page_source, "html.parser")
        #code = soup.find_all("div", attrs={"class":"ace_line"})
        script = soup.find("script", text=re.compile("submissionCode:"))
        code = re.findall("submissionCode:\s*'(.+)'",script.string)[0].decode("unicode-escape")
        suff = suffix_conversion(re.findall("getLangDisplay:\s*'(.+)'",script.string)[0])


        id = str(ac["id"])
        if len(id) < 2:
            id = "00" + id
        elif len(id) < 3:
            id = "0" + id

        folderName = id + ". " + ac["title"]
        if not os.path.exists(directory + "\\" + folderName):
            os.makedirs(directory + "\\" + folderName)
        
        completeName = os.path.join(directory + "\\" + folderName, "{}.{}".format("Solution", suff))         
        if not os.path.exists(completeName):
            print(folderName + " saved.")
            file = open(completeName, "w")
            file.write(code)
            file.close()
        elif os.path.exists(completeName) and overWrite.lower() == "yes":
            print(folderName + " over-written.")
            file = open(completeName, "w")
            file.write(code)
            file.close()
        elif os.path.exists(completeName) and overWrite.lower() == "no":
            print(folderName + " skipped.")

def get_ac_problem_list():
    ac_list = []
    url = "https://leetcode.com/api/problems/algorithms/"
    
    driver.get(url);
    pageSource = driver.page_source
    jsonObj = json.loads(driver.find_element_by_tag_name("body").text)
    
    for ac in jsonObj["stat_status_pairs"]:
        if ac["status"] == "ac":
           
            url = "https://leetcode.com/problems/" + ac["stat"]["question__title_slug"] + "/submissions"
            
            ac_info = {
                "id" : ac["stat"]["question_id"],
                "title" : ac["stat"]["question__title"],
                "url" : url
                }
            ac_list.append(ac_info)
    
    return ac_list


def login():
    login_url = "https://leetcode.com/accounts/login/"

    if Account and Password:
        driver.get(login_url)

        username = driver.find_element_by_id("id_login")
        password = driver.find_element_by_id("id_password")
        
        username.send_keys(Account)
        password.send_keys(Password)

        driver.find_element_by_name("signin_btn").click()

        delay = 5 # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "home-app")))
            #print "Page is ready!"
        except TimeoutException:
            print "Loading took too much time!"
        
def suffix_conversion(suff="cpp"):
    if suff in suffix:
        return suffix[suff]

if __name__ == "__main__":
    login()
    ac_list = get_ac_problem_list()
    if len(ac_list) == 0:
        print("Sorry, it seems that you haven't solved any problem yet.")
    elif len(ac_list) > 0:
        print(str(len(ac_list)) + " AC solutions detected...")
        save_ac_code(ac_list)
    
    driver.quit()