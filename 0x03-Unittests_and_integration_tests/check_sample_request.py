import requests
import io
import PyPDF2


 
url = "https://arxiv.org/pdf/2504.16068"
response = requests.get(url)

with io.BytesIO(response.content) as open_pdf_file:
    reader = PyPDF2.PdfReader(open_pdf_file)
    for page in reader.pages:
        text = page.extract_text()
        print(text)