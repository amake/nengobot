from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nengobot',
    version='1.0',
    description='A bot to tweet predictions for the new Japanese era name',
    long_description=long_description,
    url='https://github.com/amake/nengobot',
    author='Aaron Madlon-Kay',
    author_email='aaron@madlon-kay.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='kanji hanzi ring twitter bot',
    py_modules=['nengo', 'bot', 'announce'],
    install_requires=['tweepy', 'pillow']
)
