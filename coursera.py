from lxml import etree
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



def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_amount = 3
    print(get_course_info(get_courses_list(url, courses_amount)))
    # course_url = 'https://www.coursera.org/learn/story-writing-project'
    # course_html = requests.get(course_url)
    # page_1 = lxml.html.document_fromstring(course_html.text)
    # print(len(page_1.find_class('week')))
    # print(page_1.find_class('ratings-text bt3-visible-xs')[0].text_content())
    # print(page_1.find_class('startdate rc-StartDateString caption-text')[0].text_content())
    # print(page_1.find_class('language-info')[0].text_content())
    # print(page_1.find_class('title display-3-text')[0].text_content())
