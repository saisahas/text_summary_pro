import pytesseract
pytesseract.pytesseract.tesseract_cmd=r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import cv2
import numpy as np
import PyPDF2 
import textract
from nltk.corpus import stopwords
import os
encoding = 'utf-8'

def text_extraction(filename):

    pdfFileObj = open(filename,'rb')

    # (filename,'rb')
    #The pdfReader variable is a readable object that will be parsed.
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #Discerning the number of pages will allow us to parse through all the pages.
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    #The while loop will read each page.
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    #This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.
    if text != "":
        text = text
    #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
    else:
        text = textract.process(filename, method='tesseract', language='eng')
    
    if type(text) == bytes:
        text = text.decode(encoding)
    else:
        text
    #converting bytes to string
    #extracted_text = text.decode(encoding)
    return(text)
    
    

