from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import PyPDF2,sys,re


class pdf_access:
    path=''
    def __init__(self,path,file_password=''):
        self.text=[]
        self.path=path
        self.reader=PyPDF2.PdfFileReader(open(path,'rb'))
        self.pgno=self.reader.getNumPages()
        self.rsrcmgr = PDFResourceManager()
        self.retstr = StringIO()
        self.codec = 'utf-8'
        self.laparams = LAParams()
        self.device = TextConverter(self.rsrcmgr, self.retstr, codec=self.codec, laparams=self.laparams)
        self.fp = open(path, 'rb')
        self.interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)
        self.password =file_password 
        self.maxpages = 1
        self.caching = False
        for i in range(self.pgno):
            inside=[i]
            pagenos=set(inside)
        
            for page in PDFPage.get_pages(self.fp, pagenos, maxpages=self.maxpages, password=self.password, check_extractable=True):
                self.interpreter.process_page(page)
                self.text .append(self.retstr.getvalue())
                self.retstr.truncate(0)
        l1=[]
        for ip in self.text:
            ip=re.sub(r'\x00+',' ',ip)
            ip=re.sub(r'\s+', ' ', ip)
            l1.append(ip)
        self.text=l1
    def get_text(self):
        return(''.join(self.text))
    def print(self):
        print(*self.text)
    def getpage(self,i):
        return(self.text[i-1])
    def search_pdf(self,keyword):
        ans=[]
        count=0
        for i in self.text:
            count=count+1
            for lines in i.split('\n\n'):
                if keyword in lines:
                    ans.append('pg--------'+str(count))
                    ans.append(lines)
                    flag=1
        if flag!=1:ans.append("keyword not found")
        return ans
def main(path=''):
    if path == "":
        path=input('enter pdf path ')
        print('please wait this may take a minute')
    obj=pdf_access(path)
    return (obj)

def get_text(obj):
    return(obj.get_text())    
def print_it(obj):
    return(obj.print())

def search_pdf(obj,key):
    return(obj.search_pdf(key))

def get_page(obj):
    return(obj.getpage(int(input('enter page number ='))))

def choose(obj):
    while True:
        opt=input('enter operation to do \n 1.Print \n 2. Get Page \n 3. Search \n 4.Exit \noption ')
        if opt=='1':
            print(print_it(obj))
        elif opt=='2':
            print(get_page(obj))
        elif opt=='3':
            ans=search_pdf(obj,input('enter keyword to search ='))
            for i in ans:print (i)
        elif opt=='4':
            break
        else:print('enter one number from the option and no text =')
    print('Thank You')
if __name__=='__main__':
    obj=main()
    choose(obj)
