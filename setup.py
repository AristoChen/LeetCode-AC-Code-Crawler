from setuptools import setup

setup(
    name = 'LeetCode AC Code Crawler',
    version = '0.3',
    description = 'Saved all accepted code on LeetCode',
    classifiers = [
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    author = 'AristoChen',
    install_requires=['bs4', 'beautifulsoup4',
                        'selenium', 'chromedriver-autoinstaller', 'certifi']
)
