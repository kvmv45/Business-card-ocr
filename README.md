# AI Business Card Reader

## Overview
The AI Business Card Reader is a web application that utilizes Optical Character Recognition (OCR) technology to extract information from business cards. Built with EasyOCR, OpenCV, and Streamlit, this application allows users to upload images of business cards and automatically extract relevant details such as the cardholder's name, company name, contact number, email, and more. The extracted data can also be stored in a MySQL database for future reference.

## Features
- Upload images of business cards in JPG, JPEG, or PNG format.
- Extracts key information including:
  - Cardholder Name
  - Company Name
  - Designation
  - Contact Number
  - Email Address
  - Website URL
  - Pincode
  - Address
  - City
  - State
- Store extracted data in a MySQL database.
- Retrieve and display previously stored information.

## Technologies Used
- Python
- EasyOCR
- OpenCV
- Streamlit
- MySQL
- NumPy
- Pandas
- Regular Expressions (re)

## Installation

### Prerequisites
- Python 3.7 or higher
- MySQL Server

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-business-card-reader.git
   cd ai-business-card-reader

**Install required packages:**
pip install easyocr opencv-python streamlit mysql-connector-python pandas numpy

**Set up the MySQL database:**
Open your MySQL client and execute the following commands:
CREATE DATABASE IF NOT EXISTS card_details;
USE card_details;
CREATE TABLE IF NOT EXISTS card_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Card_holder_Name VARCHAR(255),
    Company_name VARCHAR(255),
    Designation VARCHAR(255),
    Contact_number VARCHAR(255),
    Email VARCHAR(255),
    Website_url VARCHAR(255),
    Pincode VARCHAR(255),
    Address VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(255),
    image LONGBLOB
);

**Run the Streamlit application:**
streamlit run app.py
