# LeetCode-AC-Code-Crawler

### Origin

It is time consuming to copy and paste hundreds of problems that I solved on LeetCode, so I decided to write a crawler instead.

At the begining, I found a useful dependency in python called ```BeautifulSoup```, but it seems that it is not able to deal with dynamic website, which means that if some elements shown in a website is controlled by javascript. After searching for a while, I found ```selenium```, which automatically controll website like a human, but it seems that it is unefficient to use selenium to parse data in html, so I combine BeautifulSoup and selenium to finish this project.

### Install Dependencies

```
# python3 setup.py install
```

Note: python2 is now not supported, unless there is a need. Feel free to let me know.

### Install ChromeDriver

This project use [Chromedriver](http://chromedriver.chromium.org/) in selenium, before running this project, you have to add the downloaded executable file to PATH enviroment variable, or if your python version is greater than 3.5, than you can enable chromedriver auto install by setting `true` in `["Chromedriver"]["AutoInstall"]` in `conf.json`.

Note: [Chromedriver-autoinstaller](https://github.com/yeongbin-jo/python-chromedriver-autoinstaller) is a open source project, it is indeed convenient, but there are still some limitations, and if you are having issue using it, maybe consider manually download Chromedriver by yourself.

### Setting

You have to modify variables in `conf.json`.
```json
{
    "Username": "YOUR_USERNAME",
    "Password": "YOUR_PASSWORD",
    "OutputDir": "THE_ABSOLUTE_PATH_THAT_YOU_WANT_TO_SAVE_FILES",
    "Chromedriver": {
        "AutoInstall": false,
        "Path": "THE_ABSOLUTE_PATH_OF_CHROMEDRIVER"
    },
    "Headless": true,
    "Overwrite": false
}
```

#### Execute
After executing the project, each LeetCode problem that you've solved will have a folder containing a file named "Solution" with the language you used as its suffix. 

I tried this project on Windows10 & Ubuntu, and it works fine. 

#### Notice 
- If you have multiple sessions in your account, switch to the session that you want to crawl ac codes before execute.
- If you set the `Headless` to `true`, and keep seeing `Loading took too much time!` message, maybe it's the Google reCAPTCHA causing the problem, this software is not able to handle this problem, you need to set the `Headless` to `false`, run the software again and then manually pass the Google reCAPTCHA testing.
