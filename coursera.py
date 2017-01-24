from lxml import etree
from openpyxl import Workbook
import lxml.html
import random
import requests


def get_courses_list(url, courses_amount):
    xml_request = requests.get(url)
    root = etree.XML(xml_request.content)
    courses_list = []
    for child in root:
        for link in child:
            courses_list.append(link.text)
    return random.sample(courses_list, courses_amount)


def download_course(course_url):
    course_request = requests.get(course_url)
    course_page = lxml.html.document_fromstring(course_request.text)
    return course_page


def get_courses_info_from_list(courses_list):
    all_course_info_list = []
    for course in courses_list:
        course_page = download_course(course)
        course_info = get_course_info(course_page)
        all_course_info_list.append(course_info)
    return all_course_info_list


def get_course_class_content(course_page, class_name):
    try:
        return course_page.find_class(class_name)[0].text_content()
    except IndexError:
        return None


def get_course_info(course_page):
    course_name = get_course_class_content(course_page, 'title display-3-text')
    course_lang = get_course_class_content(course_page, 'language-info')
    course_starts = get_course_class_content(course_page, 'startdate rc-StartDateString caption-text')
    course_rating = get_course_class_content(course_page, 'ratings-text bt3-visible-xs')
    course_length = len(course_page.find_class('week'))
    course_sum = (course_name, course_lang, course_starts, course_length, course_rating)
    return course_sum


def output_courses_info_to_xlsx(all_courses_info_list):
    excel_file = Workbook()
    ex_page_1 = excel_file.active
    ex_page_1.title = 'Coursera random courses info'
    ex_page_1['A1'] = 'Name'
    ex_page_1['B1'] = 'Language'
    ex_page_1['C1'] = 'Start date'
    ex_page_1['D1'] = 'Length (weeks)'
    ex_page_1['E1'] = 'Rating'
    row = 2
    for course_info in all_courses_info_list:
        ex_page_1['A' + str(row)] = course_info[0]
        ex_page_1['B' + str(row)] = course_info[1]
        ex_page_1['C' + str(row)] = course_info[2]
        ex_page_1['D' + str(row)] = course_info[3]
        ex_page_1['E' + str(row)] = course_info[4]
        row += 1
    excel_file.save('Courses.xlsx')


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_amount = 5
    courses_list = get_courses_list(url, courses_amount)
    all_course_info_list = get_courses_info_from_list(courses_list)
    output_courses_info_to_xlsx(all_course_info_list)
