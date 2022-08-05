import os,requests, utils.helpers as helpers, db, json
from bs4 import BeautifulSoup
from pages import PAGES


def get_credentials():

    try:
        if os.environ.get('MODE') == 'DEVELOPMENT':
            from credentials import set_credentials
            set_credentials()

            print('Development database in use - Main, line 13')
            return json.loads(os.environ.get('DATABASE_URL'))
        else:
            print('Production database in use - Main, line 16')
            return os.environ['DATABASE_URL']

    except:
        print('Problem Retrieving Database URL')


SOURCE_EMAIL_ADDRESS = os.environ.get('SOURCE_EMAIL_ADDRESS')
SOURCE_EMAIL_PASSWORD = os.environ.get('SOURCE_EMAIL_PASSWORD')
DESTINATION_EMAIL_ADDRESS = os.environ.get('DESTINATION_EMAIL_ADDRESS')


def get_page(database_url, page_url, page_attributes_tag, page_attribute_tag_attribute):
    db.create_table(database_url, 'web_pages', page_url)

    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    scraped_page = str(soup.find(page_attributes_tag, page_attribute_tag_attribute))

    saved_page_data = db.read_from_db(database_url, 'web_pages', 'data', page_url)

    helpers.compare_pages(db, database_url, page_url, saved_page_data, scraped_page, SOURCE_EMAIL_ADDRESS, SOURCE_EMAIL_PASSWORD, DESTINATION_EMAIL_ADDRESS)

    return 


def main(pages):

    #os.environ['MODE'] = 'DEVELOPMENT'

    database_url = get_credentials()

    for i in range(len(pages)):
        page_url = pages[i]['url']
        tag = pages[i]['tag']
        tag_attribute = pages[i]['tag_attribute']
        get_page(database_url, page_url, tag, tag_attribute)
    return

main(PAGES)