# LeetCode-AC-Code-Crawler

#### Origin
I've been solving LeetCode problems recently, and when I realized that why not put my solutions on github, I found it time consuming to copy and paste hundreds of problems that I solved, so I decided to write a crawler instead.

At the begining, I found a useful dependency in python called ```BeautifulSoup```, but it seems that it is not able to deal with dynamic website, which means that if some elements shown in a website is controlled by javascript. After serching for a while, I found ```selenium```, which automatically controll website like a human, but it seems that it is unefficient to use selenium to parse data in html, so I combine BeautifulSoup and selenium to finish this project.

#### Install Dependencies
```
# pip install bs4
# pip install beautifulsoup
# pip install selenium 
```

#### Install ChromeDriver 
This project use [Chromedriver](http://chromedriver.chromium.org/) in selenium, before running this project, you have to add the downloaded executable file to PATH enviroment variable.

#### Setting
You have to modify variables in `conf.json`.
```json
{
    "Username": "YOUR_USERNAME",
    "Password": "YOUR_PASSWORD",
    "OutputDir": "THE_ABSOLUTE_PATH_THAT_YOU_WANT_TO_SAVE_FILES",
    "ChromedriverPath": "THE_ABSOLUTE_PATH_OF_CHROMEDRIVER"
}
```

#### Execute
After executing the project, each LeetCode problem that you've solved will have a folder containing a file named "Solution" with the language you used as its suffix. 

I tried this project on Windows10 & Ubuntu, and it works fine. 

#### Notice 
If you have multiple sessions in your account, switch to the session that you want to crawl ac codes before execute.
