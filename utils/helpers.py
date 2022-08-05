import smtplib
from utils.email_template import create_email


def send_email(source_email_address, source_email_password, message):
    print('attempting to send email')
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        print('email server initialized')
        server.ehlo()
        print('opening TLS')
        server.starttls()
        print('ehlo')
        server.ehlo()
        print('logging into source email')
        server.login(source_email_address, source_email_password)
        print('logged in. Sending email')
        server.send_message(message)
        print('email sent')


def compare_pages(db, database_url, saved_page_url, saved_page_data, scraped_page, source_email_address, source_email_password, destination_email_address, email_title=None, email_message=None):
    print(f'pages difference {saved_page_data[0] != scraped_page}')
    if saved_page_data[0] != scraped_page:
        print('updating table')
        db.update_table(database_url, 'web_pages', 'data', saved_page_url, scraped_page)

        print(f'{saved_page_url} - STATUS: UPDATED')

        print('creating email')
        message = create_email(source_email_address, destination_email_address, saved_page_url, email_title, email_message)

        print('sending email')
        try:
            send_email(source_email_address, source_email_password, message)
        except:
            print('Unable to send email')

        return

    print(f'{saved_page_url} - STATUS: NO UPDATE')

    return

