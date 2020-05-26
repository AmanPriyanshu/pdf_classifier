import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io

def pdfparser(data, f_pgs, l_pgs):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'ascii'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    c = 0
    for page in PDFPage.get_pages(fp):

        c += 1
        if c < f_pgs:
            continue

        interpreter.process_page(page)
        data =  retstr.getvalue()

        if l_pgs == -1:
            continue
        if c >= l_pgs:
            break

    return data

if __name__ == '__main__':
    pdfparser(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))