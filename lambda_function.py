from bs4 import BeautifulSoup
import lxml
import requests,  openpyxl
from csv import writer
import os

def lambda_handler(event, context):
    #SAVING TO EXCEL
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = 'Hotelsng Best Hotel Data'
    sheet.append(['Hotel Name', 'Address', 'Facilities', 'Price(N)', 'Review', 'Ratings', 'Likes', 'URL'])

    try:
        
        for i in range(46):
            
            url = requests.get('https://hotels.ng/hotels-in-lagos/best/{}'.format(i+1)).text
            content = url

            soup = BeautifulSoup(content, 'html.parser')

            all_hotels = soup.find("div", {"id": 'topPicks'})

            hotels = all_hotels.find_all('div', attrs={'class':'listing-hotels'})

            for hotel in hotels:
                
                if hotel.find('h2') == None:
                    continue
                    
                elif hotel.find('p') == None:
                    continue

                elif hotel.find('blockquote') == None:
                    continue

                elif hotel.find('div') == None:
                    continue

                elif hotel.find('a') == None:
                    continue
                    
                name = hotel.find('h2', class_='listing-hotels-name').text
                address = hotel.find('p', class_='listing-hotels-address').text
                facilities= hotel.find('div', class_='listing-hotels-facilities').get_text(',', strip = True)
                price = hotel.find('p', class_ ='listing-hotels-prices-discount').get_text(' ', strip = True).strip('₦')
                review = hotel.find('blockquote').get_text(strip = True)
                rating = hotel.find('p', class_='listing-hotels-rating').span.text.split(' ')[0]
                likes = hotel.find('div', class_='listing-hotels-likes').get_text(strip = True).split(' ')[0]
                hotel_url = hotel.find('a').get('href')


                #SAVING TO EXCEL
                sheet.append([name, address, facilities, price, review, rating, likes, hotel_url])
        
                                        

    except Exception as e:
        print(e)

    #SAVING TO EXCEL
    excel.save('/tmp/hotelsngData.xlsx')



    #SENDING THE DOCUMENT VIA EMAIL

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import ssl, email

    SENDER_EMAIL = 'codedevtestingnow@gmail.com'
    RECEIVER_EMAIL = 'wandeinks@gmail.com'
    SENDER_PASSWORD = os.environ.get('TEST_EMAIL_PASS')


    # instance of MIMEMultipart
    msg = MIMEMultipart()
    
    # storing the senders email address  
    msg['From'] = SENDER_EMAIL
    
    # storing the receivers email address 
    msg['To'] = RECEIVER_EMAIL

    # storing the subject 
    msg['Subject'] = "HotelsNG Best Hotel Information"


    # string to store the body of the mail
    body = "Kindly find the document attached"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))


    # open the file to be sent 
    filename = "hotelsngData.xlsx"
    attachment = open('/tmp/hotelsngData.xlsx', "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment", filename = filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)


    # Converts the Multipart msg into a string
    text = msg.as_string()



    context = ssl.create_default_context()

    # creates SMTP session
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # Authentication
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # sending the mail
        server.sendmail(
            SENDER_EMAIL, RECEIVER_EMAIL, text
        )

    print('Email sent successfully')

    # terminating the session
    server.close()

