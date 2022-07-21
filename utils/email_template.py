from email.message import EmailMessage

def create_email(source_email_address, destination_email_address, page_url):
    title = str(page_url).strip("https://").split('/')

    message = EmailMessage()
    message['Subject'] = f'!!!{title[0].upper()} {title[1].upper()} UPDATED!!!'
    message['From'] = source_email_address
    message['To'] = destination_email_address

    message.set_content(f'{page_url}')

    message.add_alternative(f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1>'{title[0].split('.')[1].upper()} {title[1].capitalize()} Has Been Updated! {page_url}'</h1>
            </body>
        </html>
        """, subtype='html')

    return message