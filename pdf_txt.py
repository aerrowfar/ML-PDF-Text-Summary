import PyPDF2
import textract
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import io

input_file='sample.pdf'


#get how many pages of text in pdf
def get_num_pages(input_file):
    pdf_file = open(input_file, 'rb')
    pypdf_file = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pypdf_file.numPages
    return num_pages


#get text of a pdf
def pdf_to_text_miner(input_file):
    inFile=open(input_file,'rb')
    resMgr= PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
    interpreter=PDFPageInterpreter(resMgr, TxtConverter)

    for page in PDFPage.get_pages(inFile):
        interpreter.process_page(page)
    
    txt= retData.getvalue()

    return txt
    

 
#get text of a pdf at specific page
def pdf_to_text(input_file,i):
    pdf_file = open(input_file, 'rb')

    #a readable object for PyPDF
    pypdf_file = PyPDF2.PdfFileReader(pdf_file)

    num_pages = i
    count= 0 
    text=''

    page=pypdf_file.getPage(i)
    text = page.extractText()

    #if PyPDF worked, return text
    if text != '':
        return text
    #PyPDF didnt work, must mean its a scanned page, use textract instead
    else:
        text = textract.process(input_file, method='tesseract', language='eng')
        return text


#Two pdf to text methods available, comment out the one you dont want.
if __name__=='__main__':
    text= pdf_to_text(input_file)
    #text= pdf_to_text_miner(input_file, i)

    print(text)