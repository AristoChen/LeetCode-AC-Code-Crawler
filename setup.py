from setuptools import setup

setup(
    name = 'LeetCode AC Code Crawler',
    version = '0.1',
    description = 'Saved all accepted code on LeetCode',
    classifiers = [
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    author = 'AristoChen',
    install_requires = ['bs4', 'beautifulsoup', 'selenium']
)