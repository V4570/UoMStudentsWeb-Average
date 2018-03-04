from bs4 import BeautifulSoup as bs
import argparse
import sys
import yaml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

with open('config.yaml', 'r') as in_stream:
    CONFIG = yaml.safe_load(in_stream)


def selenium_login_data_extract():
    
    username = CONFIG['username']
    
    password = CONFIG['password']

    login_url = CONFIG['login_url']

    grades_url = CONFIG['grades_url']

    browser = webdriver.Firefox()
    browser.get(login_url)
    _username = browser.find_element_by_name("userName")
    _password = browser.find_element_by_name("pwd")

    _username.send_keys(username)
    _password.send_keys(password)
    browser.find_element_by_name("submit1").click()
    browser.get(grades_url)
    
    soup = bs(browser.page_source, 'html.parser')
    browser.quit()
    grades_table = soup.find(id='mainTable').find('table').findChildren('tr', {'height' : '25','bgcolor' : '#fafafa'})
    return grades_table


def get_grades(grades):
    normalized_grades = []

    for tr in grades:
        tds = tr.findChildren('td')
        fix = tds[1].contents[0].split()
        del(fix[0])
        
        course_title = ' '.join(fix)
        ects = int(tds[5].contents[0].strip())
        
        try:
            grade = int(tds[6].find('span').contents[0].strip())
        except ValueError:
            grade = tds[6].find('span').contents[0].strip()
        
        course = {'title': course_title, 'grade' : grade, 'ects' : ects}
        
        normalized_grades.append(course)

    return normalized_grades


def calculate_average(normalized_grades):
    english_courses = ['ΑΓΓΛΙΚΑ II', 'ΑΓΓΛΙΚΑ III', 'ΑΓΓΛΙΚΑ IV']
    
    max_english = max(course['grade'] * course['ects'] for course in normalized_grades
        if course['grade'] != '-'
            and course['grade'] >= 5
            and course['title'] in english_courses)
    
    total_ects = sum(course['ects'] for course in normalized_grades
        if course['grade'] != '-' and course['grade']>=5) - 10
    
    total_grades = sum(course['grade'] * course['ects'] for course in normalized_grades
        if course['grade'] != '-'
            and course['grade']>=5
            and course['title'] not in english_courses)
    total_grades += max_english
    
    avg = round(total_grades/total_ects, 2)
    return avg



if __name__ == '__main__':

    grades = selenium_login_data_extract()
    normalized_grades = get_grades(grades)
    avg = calculate_average(normalized_grades)
    
    for course in normalized_grades:
        title = course['title']
        sys.stdout.write('{} : {}\n'.format(title, course['grade']))
    sys.stdout.write('Average Grade: {}'.format(avg))
