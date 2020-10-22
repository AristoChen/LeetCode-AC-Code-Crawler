from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import codecs
import json
import time
import re
import os
import sys

username = ""
password = ""
outputDir = ""
driver = ""
overwrite = False

timeout = 5 # second

suffix = {"cpp": "cpp", "c": "c", "csharp": "cs", "golang": "go",
          "java": "java", "javascript": "js", "kotlin": "kt", "php": "php",
          "python": "py", "python3": "py", "ruby": "rb", "rust": "rs",
          "scala": "scala", "swift": "swift", "typescript": "ts"}

def save_ac_code(ac_list, premium):
    premium_count = 0
    processed_nums = 0

    level = ["None", "Easy", "Medium", "Hard"]

    start_time = time.time()

    for ac in reversed(ac_list):

        if ac["paid_only"] == True:
            premium_count += 1
            if not premium:
                print(str(ac["id"]) + ". " + ac["title"] + " is a premium problem, not able to access") 
                continue

        url = ac["url"]
        difficulty = level[ac["difficulty"]]
        ac_submission_list = ""

        while len(ac_submission_list) == 0:
            driver.get(url)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ac_submission_list = soup.find_all("a", text="Accepted")

        for i in range(len(ac_submission_list)):
            driver.get("https://leetcode.com" + ac_submission_list[i]["href"])
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Get submission details
            testcase = soup.find("span", id = "result_progress").text
            runtime = soup.find("span", id = "result_runtime").text
            ranking = soup.find("div", style="line-height: 1em; position: relative;")
            if ranking:
                ranking = ranking.text.replace("\n", " ").replace("              ", "")[15:]
            else:
                ranking = "Your runtime beats 00.00 % of submissions."
            submission_detail = ("/*\n" + "Submission Detail:{" +
                                "\n    Difficulty : " + difficulty +
                                "\n    Acceptance Rate : " + str(ac["ac_rate"]*100)[:5] + " %" +
                                "\n    Runtime : " + runtime +
                                "\n    Testcase : " + testcase + " passed" +
                                "\n    Ranking : " + ranking +
                                "\n}\n*/\n\n")

            # Get ac code
            script = soup.find("script", text = re.compile("submissionCode:"))
            code = re.findall("submissionCode:\s*'(.+)'", script.string)[0]
            suff = suffix_conversion(re.findall("getLangDisplay:\s*'(.+)'", script.string)[0])

            folderName = str(ac["id"]).zfill(4) + ". " + ac["title"].strip()
            if not os.path.exists(outputDir + "\\" + folderName):
                os.makedirs(outputDir + "\\" + folderName)

            fileName = "{}.{}".format("Solution" + str(i).zfill(2), suff)
            completeName = os.path.join(
                outputDir + "\\" + folderName, fileName)
            sys.stdout.write(" "*60 + "\r")
            if not os.path.exists(completeName):
                print(folderName + "\\" + fileName + " saved.")
                file = codecs.open(completeName, "w", encoding='utf8')
                file.write(submission_detail+code)
                file.close()
            else:
                if overwrite == True:
                    print(folderName + "\\" + fileName + " overwritten.")
                    file = open(completeName, "w")
                    file.write(submission_detail+code)
                    file.close()
                else:
                    print(folderName + "\\" + fileName + " skipped.")

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

    if username and password:
        driver.get(login_url)

        usernameField = driver.find_element_by_id("id_login")
        passwordField = driver.find_element_by_id("id_password")
        
        usernameField.send_keys(username)
        passwordField.send_keys(password)

        while True:
            try:
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.ID, "signin_btn")))
                driver.find_element_by_id("signin_btn").click()
                break
            except:
                print("Unexpected error: " + str(sys.exc_info()[0]))
                time.sleep(1)

        while True:
            try:
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.ID, "home-app")))
                break
            except TimeoutException:
                print("Loading took too much time!")
    else:
        print("Username or password is empty")
        sys.exit(1)

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
    with open('conf.json', 'r') as f:
        conf = json.loads(f.read())
        username = conf["Username"]
        password = conf["Password"]
        outputDir = conf["OutputDir"]
        driverPath = conf["ChromedriverPath"]
        headless = conf["Headless"]
        overwrite = conf["Overwrite"]

    if not os.path.isdir(outputDir):
        print("Output directory not found")
        sys.exit(1)
    if not os.path.isfile(driverPath):
        print("Chromedriver not found")
        sys.exit(1)

    chrome_options = Options()
    if headless == True:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(driverPath, chrome_options=chrome_options)

    login()
    premium  = premium_account_check()
    ac_list = get_ac_problem_list()
    if len(ac_list) == 0:
        print("Sorry, it seems that you haven't solved any problem yet.")
    elif len(ac_list) > 0:
        print(str(len(ac_list)) + " AC solutions detected...")
        save_ac_code(ac_list, premium)

    driver.quit()
