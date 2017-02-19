import lxml.html
import random
import requests
from lxml import etree
from openpyxl import Workbook


def get_random_courses_list(url, courses_amount):
    xml_request = requests.get(url)
    root = etree.XML(xml_request.content)
    courses_list = [link.text for child in root for link in child]
    return random.sample(courses_list, courses_amount)


def download_course(course_url):
    course_request = requests.get(course_url)
    course_page = lxml.html.document_fromstring(course_request.text)
    return course_page


def get_courses_info_from_list(courses_list):
    return [get_course_info(download_course(course)) for course in courses_list]


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
    course_sum = {'Name': course_name,
                  'Lang': course_lang,
                  'Starts': course_starts,
                  'Length': course_length,
                  'Rating': course_rating}
    return course_sum


def create_xslx_file_workbook():
    excel_file = Workbook()
    ex_page_1 = excel_file.active
    ex_page_1.title = 'Coursera random courses info'
    ex_page_1['A1'] = 'Name'
    ex_page_1['B1'] = 'Language'
    ex_page_1['C1'] = 'Start date'
    ex_page_1['D1'] = 'Length (weeks)'
    ex_page_1['E1'] = 'Rating'
    return excel_file


def output_courses_info_to_xlsx(all_courses_info_list, excel_file):
    ex_page_1 = excel_file.active
    for row, course_info in enumerate(all_courses_info_list, start=2):
        ex_page_1['A' + str(row)] = course_info['Name']
        ex_page_1['B' + str(row)] = course_info['Lang']
        ex_page_1['C' + str(row)] = course_info['Starts']
        ex_page_1['D' + str(row)] = course_info['Length']
        ex_page_1['E' + str(row)] = course_info['Rating']
    return excel_file


def save_xlsx_file(excel_file, output_filename='Courses.xlsx'):
    excel_file.save(output_filename)
    return output_filename


def print_saved_filename(output_filename):
    print('File %s saved' % output_filename)


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_amount = 5
    courses_list = get_random_courses_list(url, courses_amount)
    all_course_info_list = get_courses_info_from_list(courses_list)
    excel_file_template = create_xslx_file_workbook()
    excel_file = output_courses_info_to_xlsx(all_course_info_list, excel_file_template)
    print_saved_filename(save_xlsx_file(excel_file))
