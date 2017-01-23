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


def get_course_info(course_slug):
    pass


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_amount = 20
    # print(get_courses_list(url, courses_amount))
