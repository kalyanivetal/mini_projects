from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import csv

page_1="https://hindishabd.com/Hindi-words-starting-with-%E0%A4%85"
def getPageData(soup):
    print("2")
    letter_2=soup.find_all('span',attrs={'class':'text-center word-items text-info'})
    #print(letter_2,len(letter_2))
    letterl2=[]
    for i in letter_2:
        word=i.text
        output=""
        for j in word:
            if j!="\n" and j!="\t":
                output+=j
                #print(output)
        letterl2.append(output)
    letterl2=list(dict.fromkeys(letterl2))
    return letterl2
    
def get_Data():
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(page_1)
        html=browser.page_source
        soup=BeautifulSoup(html,"html.parser")
        out=soup.find('tbody',attrs={'class':'dvenghinkey'})

        f_list1=[]
        f_list2=[]
        
        file1 = open('Words2_letter.csv', 'w+', newline ='') 
        file2 = open('Words3_letter.csv', 'w+', newline ='') 
        
        #print("OUT:",out,len(out))
        words=[]
        for i in out:
            for j in i:
                for k in j:
                    if k!="\n" and k!="\t":
                        #print(k)
                        words.append(k)
        print("Words are:",words)
        browser.get('https://hindishabd.com/Hindi-words-starting-with-'+words[0])
        html=browser.page_source
        soup=BeautifulSoup(html,"html.parser")
        print("In A")
        for i in words:
            new_url1='https://hindishabd.com/2-letter-Hindi-words-start-with-'+i+'?pLanguage=Hindi'
            new_url2='https://hindishabd.com/3-letter-Hindi-words-start-with-'+i+'?pLanguage=Hindi'
            
            browser.get(new_url1)
            print("Before Sleep")
            time.sleep(2)
            print("After Sleep")
            html=browser.page_source
            soup=BeautifulSoup(html,"html.parser")
            print("For URL1",new_url1)
            letters2=getPageData(soup)
            if len(letters2)>0:
                print("Letters 2:",i,letters2,len(letters2))
                f_list1.append(letters2)

            browser.get(new_url2)
            print("Before Sleep")
            time.sleep(2)
            print("After Sleep")
            html=browser.page_source
            soup=BeautifulSoup(html,"html.parser")
            print("For URL2",new_url1)
            letters3=getPageData(soup)
            print("Letters 3:",i,letters3,len(letters3))
            if len(letters3)>0:
                f_list2.append(letters3)
                print(f_list1,len(f_list1))
            
            d = [letters2, letters3]
        
        #export_data = zip_longest(*f_list, fillvalue = '')
        
        print(f_list1,len(f_list1))
        print(f_list2,len(f_list2))
        with file1:
            write = csv.writer(file1)
            write.writerows(f_list1)
        with file2:
            write = csv.writer(file2)
            write.writerows(f_list2)

    except TimeoutException as e:
        print(e)
        print("Timeout")
        browser.close()

if __name__=="__main__":
    get_Data()

