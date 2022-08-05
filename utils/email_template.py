from email.message import EmailMessage

def create_email(source_email_address, destination_email_address, page_url, email_title, email_message):
    print('creating email')

    title = str(page_url).strip("https://").split('/')

    message = EmailMessage()

    print('setting email source')
    message['From'] = source_email_address

    print('setting email destination')
    message['To'] = destination_email_address
    
    print('setting email subject')
    if email_title:
        print('email title not None')
        message['Subject'] = email_title

    else:
        print('email title is None. generating title')

        message['Subject'] = f'!!!{title[0].upper()} {title[1].upper()} UPDATED!!!'
    print('email title created')
    

    message.set_content(f'{page_url}')

    print('setting email message')
    if email_message is not None:
        print('email message not None')

        message.add_alternative(f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1>'{email_message} {page_url}'</h1>
            </body>
        </html>
        """, subtype='html')

    else: 
        print('email message is None. generating message')
        message.add_alternative(f"""\
            <!DOCTYPE html>
            <html>
                <body>
                    <h1>'{title[0].split('.')[1].upper()} {title[1].capitalize()} Has Been Updated! {page_url}'</h1>
                </body>
            </html>
            """, subtype='html')

    print(f'email created')

    return message