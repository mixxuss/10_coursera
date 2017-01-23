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


def get_course_info(courses_url_list):
    all_courses_info_list = []
    for course_url in courses_url_list:
        course_request = requests.get(course_url)
        course_page = lxml.html.document_fromstring(course_request.text)
        course_name = course_page.find_class('title display-3-text')[0].text_content()
        course_lang = course_page.find_class('language-info')[0].text_content()
        course_starts = course_page.find_class('startdate rc-StartDateString caption-text')[0].text_content()
        course_length = len(course_page.find_class('week'))
        course_rating = course_page.find_class('ratings-text bt3-visible-xs')[0].text_content()
        course_sum = (course_url, course_name, course_lang, course_starts, course_length, course_rating)
        all_courses_info_list.append(course_sum)
    return all_courses_info_list


def output_courses_info_to_xlsx(all_courses_info_list):
    excel_file = Workbook()
    ex_page_1 = excel_file.active
    ex_page_1.title = 'Coursera random courses info'
    ex_page_1['A1'] = 'URL'
    ex_page_1['B1'] = 'Name'
    ex_page_1['C1'] = 'Language'
    ex_page_1['D1'] = 'Start date'
    ex_page_1['E1'] = 'Length'
    ex_page_1['F1'] = 'Rating'
    row = 2
    for course_info in all_courses_info_list:
        ex_page_1['A' + row] = course_info[0]
        ex_page_1['B' + row] = course_info[1]
        ex_page_1['C' + row] = course_info[2]
        ex_page_1['D' + row] = course_info[3]
        ex_page_1['E' + row] = course_info[4]
        ex_page_1['F' + row] = course_info[5]
        row += 1
    excel_file.save('Courses.xlsx')


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_amount = 5
    all_course_info_list = get_course_info(get_courses_list(url, courses_amount))
    output_courses_info_to_xlsx(all_course_info_list)







    # print(get_course_info(get_courses_list(url, courses_amount)))
    # excel = Workbook()
    # filename = 'test.xlsx'
    # ws1 = excel.active
    # ws1.title = 'Coursera'
    # ws1['A1'] = 'This is A1'
    # ws1['B1'] = 'This is B1'
    # excel.save(filename=filename)






    # course_url = 'https://www.coursera.org/learn/story-writing-project'
    # course_html = requests.get(course_url)
    # page_1 = lxml.html.document_fromstring(course_html.text)
    # print(len(page_1.find_class('week')))
    # print(page_1.find_class('ratings-text bt3-visible-xs')[0].text_content())
    # print(page_1.find_class('startdate rc-StartDateString caption-text')[0].text_content())
    # print(page_1.find_class('language-info')[0].text_content())
    # print(page_1.find_class('title display-3-text')[0].text_content())
