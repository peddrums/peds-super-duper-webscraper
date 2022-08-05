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


def get_page(database_url, page_url, page_attributes_tag, page_attribute_tag_attribute, source_email_address, source_email_password, destination_email_address, email_title=None, email_message=None):
    db.create_table(database_url, 'web_pages', page_url)


    print('scrape: table created. Getting page')
    r = requests.get(page_url)
    print('scrape: got page')

    print('scrape: parsing html')
    soup = BeautifulSoup(r.text, 'html.parser')
    scraped_page = str(soup.find(page_attributes_tag, page_attribute_tag_attribute))

    print('reading previous page scrape data')
    saved_page_data = db.read_from_db(database_url, 'web_pages', 'data', page_url)
    print('previous scrape data retrieved')

    print('comparing pages')
    helpers.compare_pages(db, database_url, page_url, saved_page_data, scraped_page, source_email_address, source_email_password, destination_email_address, email_title, email_message)
    print('scrape completed')

    return 


def main(pages):

    #os.environ['MODE'] = 'DEVELOPMENT'

    database_url = get_credentials()


    source_email_address = os.environ.get('SOURCE_EMAIL_ADDRESS')
    source_email_password = os.environ.get('SOURCE_EMAIL_PASSWORD')
    destination_email_address = os.environ.get('DESTINATION_EMAIL_ADDRESS')


    for i in range(len(pages)):
        page_url = pages[i]['url']
        tag = pages[i]['tag']
        tag_attribute = pages[i]['tag_attribute']

        email_title=None
        email_message=None

        if pages[i]['email_title']:
            email_title = pages[i]['email_title']
        
        if pages[i]['email_message']:
            email_message = pages[i]['email_message']

        get_page(database_url, page_url, tag, tag_attribute, source_email_address, source_email_password, destination_email_address, email_title, email_message)

    return

main(PAGES)