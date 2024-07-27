# Required Libraries/Modules
import easyocr # type: ignore
import cv2 # type: ignore
import numpy as np # type: ignore
import PIL.Image as Image # type: ignore
import re
import pandas as pd # type: ignore
import streamlit as st # type: ignore
import mysql.connector  # type: ignore
import time

# Set up the page configuration
st.set_page_config(
    page_title="AI Business Card Reader",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Kirthivasan's Dashboard!"}
)
st.title(':violet[AI Business Card Reader]')

# Connect to MySQL
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Kirthi@123'
)
mycursor = mydb.cursor()
mycursor.execute("Create Database IF NOT EXISTS card_details")
mycursor.execute("use card_details")
mycursor.execute('''Create Table IF NOT EXISTS card_info(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       Card_holder_Name varchar(255),
                       Company_name varchar(255),
                       Designation varchar(255),
                       Contact_number varchar(255),
                       Email varchar(255),
                       Website_url varchar(255),
                       Pincode varchar(255),
                       Address varchar(255),
                       City varchar(255),
                       State varchar(255),
                       image LONGBLOB )
                 ''')

# Upload & Extract functionality
st.subheader(":blue[Upload & Extract]")

image = st.file_uploader("Choose an image of a business card", type=["jpg", "jpeg", "png"])

if image is not None:
    file_bytes = image.read()
    nparr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, channels='BGR', width=450, caption="Uploaded image")

    with col2:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(np.array(image), detail=0)
        card = " ".join(result)  # Convert to string

        replacing = [
            (';', ""),
            (',', ''),
            ('.com', 'com'),
            ('com', '.com'),
            ('WWW ', 'www.'),
            ("www ", "www."),
            ('www', 'www.'),
            ('www.', 'www'),
            ('wWW', 'www'),
            ('wwW', 'www')
        ]
        for old, new in replacing:
            card = card.replace(old, new)

        # Extracting phone number
        phone_pattern = r"\+*\d{2,3}-\d{3,4}-\d{4}"
        match1 = re.findall(phone_pattern, card)
        Phone = ''
        for phone in match1:
            Phone = Phone + ' ' + phone
            card = card.replace(phone, "")

        # Extracting pincode
        pin_code = r"\d+"
        Pincode = ''
        match2 = re.findall(pin_code, card)
        for code in match2:
            if len(code) == 6 or len(code) == 7:
                Pincode = Pincode + code
                card = card.replace(code, "")

        # Extracting email id
        email_id = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}\b"
        Email_id = ''
        match3 = re.findall(email_id, card)
        for ids in match3:
            Email_id = Email_id + ids
            card = card.replace(ids, '')

        # Extracting web url
        web_url = r"www\.[A-Za-z0-9]+\.[A-Za-z]{2,3}"
        Web_Url = ''
        match4 = re.findall(web_url, card)
        for url in match4:
            Web_Url = url + Web_Url
            card = card.replace(url, "")

        # Extracting alpha words from the result
        alpha_patterns = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
        alpha_var = []
        for i in result:
            if re.findall(alpha_patterns, i):
                if i not in 'WWW':
                    alpha_var.append(i)
                    card = card.replace(i, "")

        # Extracting name
        Card_holder_Name = alpha_var[0]

        # Extracting company name
        Company_name = alpha_var[2] if len(alpha_var) == 3 else alpha_var[2] + " " + alpha_var[3]

        st.write(':red[Name]:', Card_holder_Name)
        st.write(':red[Company name]:', Company_name)

        st.write(":violet[If you wish to upload the business card data and an image to a database, please click the below button.]")

        submit = st.button("Upload data")

        if submit:
            with st.spinner("Please wait...."):
                time.sleep(5)
                sql = "INSERT INTO card_info(Card_holder_Name,Company_name,Designation,Contact_number,Email,Website_url,Pincode,Address,City,State,image) " \
                      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (Card_holder_Name, Company_name, alpha_var[1], Phone, Email_id, Web_Url, Pincode, card, card.split()[2], card.split()[3], file_bytes)
                mycursor.execute(sql, val)
                mydb.commit()
                st.success('Done, Uploaded to database successfully')

    # Retrieve information from the database if the fields match
    mycursor.execute("SELECT Card_holder_Name, Company_name FROM card_info WHERE Card_holder_Name = %s AND Company_name = %s",
                     (Card_holder_Name, Company_name))
    db_result = mycursor.fetchone()
    if db_result:
        st.write(':green[Name from DB]:', db_result[0])
        st.write(':green[Company from DB]:', db_result[1])
