import smtplib
from utils.email_template import create_email


def send_email(source_email_address, source_email_password, message):
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(source_email_address, source_email_password)
        server.send_message(message)


def compare_pages(db, database_url, saved_page_url, saved_page_data, scraped_page, source_email_address, source_email_password, destination_email_address):

    if saved_page_data[0] != scraped_page:
        db.update_table(database_url, 'web_pages', 'data', saved_page_url, scraped_page)

        print(f'{saved_page_url} - STATUS: UPDATED')

        message = create_email(source_email_address, destination_email_address, saved_page_url)

        send_email(source_email_address, source_email_password, message)

        return

    print(f'{saved_page_url} - STATUS: NO UPDATE')

    return

