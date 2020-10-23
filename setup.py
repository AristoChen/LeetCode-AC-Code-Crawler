from setuptools import setup
import sys

if sys.version_info < (3, 0):
    setup(
        name = 'LeetCode AC Code Crawler',
        version = '0.2',
        description = 'Saved all accepted code on LeetCode',
        classifiers = [
            'Natural Language :: English',
            'Programming Language :: Python :: 2.7',
        ],
        author = 'AristoChen',
        install_requires = ['bs4', 'beautifulsoup', 'selenium']
    )
else:
    setup(
        name = 'LeetCode AC Code Crawler',
        version = '0.2',
        description = 'Saved all accepted code on LeetCode',
        classifiers = [
            'Natural Language :: English',
            'Programming Language :: Python :: 2.7',
        ],
        author = 'AristoChen',
        install_requires=['bs4', 'beautifulsoup4',
                          'selenium', 'chromedriver-autoinstaller', 'certifi']
    )
