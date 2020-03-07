from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import prompt, print_json
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from examples import custom_style_2
from broken_parsers import BrokenWebPageParsers, BrokenWebPageParser

broken_parsers = BrokenWebPageParsers()
broken_page1 = BrokenWebPageParser(url="http://craigslist.com/catvideo")
broken_page2 = BrokenWebPageParser(url="http://craigslist.com/wasup")
broken_page3 = BrokenWebPageParser(url="http://craigslist.com/mirageIII")
broken_parsers.broken_webpage_parsers = [broken_page1, broken_page2, broken_page3]

UPDATE_WEB_PARSERS = "Update broken page parsers"
ADD_NEW_SITE_TO_SCRAPE = "Add new site to scrape (todo)"
GO_BACK = 'Go Back'
welcome_questions = [
    {
        'type': 'list',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            f'{UPDATE_WEB_PARSERS} ({len(broken_parsers.broken_webpage_parsers)} broken)',
            f'{ADD_NEW_SITE_TO_SCRAPE}'
        ]
    }
]

select_webpage = [
    {
        'type': 'list',
        'name': 'page',
        'message': f'Select page to update ({len(broken_parsers.broken_webpage_parsers)} broken pages, showing 10 max at a time)',
        'choices': [{'name': x.url, 'value': x} for x in broken_parsers.broken_webpage_parsers][:10]+[GO_BACK]
    }
]

select_field = [
    {
        'type': 'list',
        'name': 'fields',
        'message': 'Select field to repair',
        'choices': [{'name': x.url, 'value': x} for x in broken_parsers.broken_webpage_parsers]
    }
]
def update_parser_for(page):
    print("let's update some fields")

answers = prompt(welcome_questions)

if UPDATE_WEB_PARSERS in answers['theme']:
    while len(broken_parsers.broken_webpage_parsers) > 0:
        page = prompt(select_webpage)
        if page['page'] == GO_BACK:
            break
        update_parser_for(page)
    print("No broken web page parsers")

elif answers['theme'] == ADD_NEW_SITE_TO_SCRAPE:
    print("Add a new site to crawl")
else:
    print(f"{answers['theme']} has no options :(")




