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
import sys

Account = "YOUR_ACCOUNT"
Password = "YOUR_PASSWORD"
directory = "THE_ABSOLUTE_PATH_THAT_YOU_WANT_TO_SAVE_FILES"
driver = webdriver.Chrome("THE_ABSOLUTE_PATH_OF_CHROMEDRIVER_THAT_YOU_JUST_INSTALLED")

suffix = {"cpp": "cpp", "cplusplus": "cpp", "c++": "cpp", "c": "c",
          "java": "java", "python": "py", "py": "py", "c#": "cs",
          "csharp": "cs", "javascript": "js", "js": "js", "ruby": "rb",
          "rb": "rb", "go": "go", "golang": "go", "swift": "swift"}

def save_ac_code(ac_list, premium):
    premium_count = 0
    processed_nums = 0

    print("Do you want to over write all files if they exists? yes/no")
    overWrite = raw_input()

    while overWrite.lower() != "yes" and overWrite.lower() != "no":
        print("Error:Please type 'yes' or 'no'")
        print("Do you want to over write all files if they exists? yes/no")
        overWrite = raw_input()

    start_time = time.time()

    for ac in reversed(ac_list):

        if ac["paid_only"] == True:
            premium_count += 1
            if not premium:
                print(str(ac["id"]) + ". " + ac["title"] + " is a premium problem, not able to access") 
                continue

        url = ac["url"]
        driver.get(url)

        level = ["None", "Easy", "Medium", "Hard"]
        difficulty = level[ac["difficulty"]]

        soup = BeautifulSoup(driver.page_source, "html.parser")
        ac_submission = soup.find_all("strong", text="Accepted")

        while len(ac_submission) == 0:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ac_submission = soup.find_all("strong", text="Accepted")

        driver.get("https://leetcode.com" + ac_submission[0].parent["href"])
        soup = BeautifulSoup(driver.page_source, "html.parser")

        #get submission details
        testcase = soup.find("span", id = "result_progress").text
        runtime = soup.find("span", id = "result_runtime").text
        ranking = soup.find("div", style="line-height: 1em; position: relative;")
        if ranking:
            ranking = ranking.text.replace("\n", " ").replace("              ", "")[15:]
        else:
            ranking = "Your runtime beats 00.00 % of cpp submissions."
        submission_detail = ("/*\n" + "Submission Detail:{" +
                             "\n    Difficulty : " + difficulty + 
                             "\n    Acceptance Rate : " + str(ac["ac_rate"]*100)[:5] + " %" +
                             "\n    Runtime : " + runtime + 
                             "\n    Testcase : " + testcase + " passed" + 
                             "\n    Ranking : " + ranking + 
                             "\n}\n*/\n\n")

        #get ac code
        script = soup.find("script", text = re.compile("submissionCode:"))
        code = re.findall("submissionCode:\s*'(.+)'", script.string)[0].decode("unicode-escape")
        suff = suffix_conversion(re.findall("getLangDisplay:\s*'(.+)'", script.string)[0])

        id = str(ac["id"])
        if len(id) < 2:
            id = "00" + id
        elif len(id) < 3:
            id = "0" + id

        folderName = id + ". " + ac["title"].strip()
        if not os.path.exists(directory + "\\" + folderName):
            os.makedirs(directory + "\\" + folderName)

        completeName = os.path.join(directory + "\\" + folderName, "{}.{}".format("Solution", suff))
        sys.stdout.write(" "*60 + "\r")         
        if not os.path.exists(completeName):
            print(folderName + " saved.")
            file = open(completeName, "w")
            file.write(submission_detail+code)
            file.close()
        elif os.path.exists(completeName) and overWrite.lower() == "yes":
            print(folderName + " over-written.")
            file = open(completeName, "w")
            file.write(submission_detail+code)
            file.close()
        elif os.path.exists(completeName) and overWrite.lower() == "no":
            print(folderName + " skipped.")

        processed_nums += 1

        end_time = time.time()
        hours, remainder = divmod(end_time-start_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        sys.stdout.write('Processed: ' + str(processed_nums) + ' / ' + str(len(ac_list)) + ' files ( Elapsed Time : {:0>2}:{:0>2}:{:0>2} ) \r'.format(int(hours),int(minutes),int(seconds)))

    if premium_count == 0 or premium:
        print("\n" + str(len(ac_list)) + " / " + str(len(ac_list)) + " completed")
    elif premium_count != 0 and not premium:
        print("\n" + str(len(ac_list)-premium_count) + " / " + str(len(ac_list)) + " completed, " +
              str(premium_count) + " / " + str(len(ac_list)) + " are premium problems, not able to access")

def get_ac_problem_list():
    ac_list = []
    url = "https://leetcode.com/api/problems/algorithms/"

    driver.get(url)
    pageSource = driver.page_source
    jsonObj = json.loads(driver.find_element_by_tag_name("body").text)

    for ac in jsonObj["stat_status_pairs"]:
        if ac["status"] == "ac":
            url = "https://leetcode.com/problems/" + ac["stat"]["question__title_slug"] + "/submissions"
            ac_info = {
                "id" : ac["stat"]["question_id"],
                "title" : ac["stat"]["question__title"],
                "difficulty" : ac["difficulty"]["level"],
                "ac_rate" : float(ac["stat"]["total_acs"]) / float(ac["stat"]["total_submitted"]),
                "paid_only" : ac["paid_only"],
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

        driver.find_element_by_id("signin_btn").click()

        delay = 5 # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "home-app")))
            #print "Page is ready!"
        except TimeoutException:
            print "Loading took too much time!"

def premium_account_check():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    subscribe = soup.find("li", {"class" : "subscribe-btn"})
    if subscribe:
        return False
    elif not subscribe:
        return True

def suffix_conversion(suff="cpp"):
    if suff in suffix:
        return suffix[suff]

if __name__ == "__main__":
    login()
    premium  = premium_account_check()
    ac_list = get_ac_problem_list()
    if len(ac_list) == 0:
        print("Sorry, it seems that you haven't solved any problem yet.")
    elif len(ac_list) > 0:
        print(str(len(ac_list)) + " AC solutions detected...")
        save_ac_code(ac_list, premium)

    driver.quit()