# UoMStudentsWeb-Average

Script that uses Selenium to login to the StudentsWeb Service, extract grades and print them and the true average.
Made it cuz i was bored of logging in every time and wanted to try selenium.

# Install requirements
> pip install -r requirements.txt

# WebDriver
You need to add geckodriver.exe(Windows) or gecko(Linux) to your path for selenium to work.

# For Linux

> chmod +x geckodriver

> export PATH=$PATH:/path-to-extracted-file/geckodriver

# Usage
You have to add your login credentials in the config.yaml file e.g. username : 'it15123' password : '123abc' and then run the script with python, preferably python 3.
