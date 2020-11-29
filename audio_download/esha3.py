from bs4 import BeautifulSoup
import csv
import os
import shutil
import time
import codecs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

url = 'https://voicemaker.in/'
hindi_akshare=['अ','अं', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ऌ', 'ऍ', 'ऎ', 'ए', 'ऐ', 'ऑ', 'ऒ', 'ओ', 'औ','अं','क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 'ऩ', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ऱ', 'ल', 'ळ', 'ऴ', 'व', 'श', 'ष', 'स', 'ह', 'क्ष', 'त्र', 'ज्ञ','ढ़','ड़']

def read_csv():
    words=[]
    with open('twoLetterWords.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[0])
            words.append(row[0].strip())

    print("Words are:",words,len(words))
    word1=words[0]
    f_list=[]
    for i in words:
        word1=i
        in_list=[]
        print(word1,len(word1))
        for l in word1:
            print(l)
            if l!=" " and l in hindi_akshare:
                print(l)
                in_list.append(l)
        print(in_list,len(in_list))
        f_list.append(in_list)
        #print(f_list,len(f_list))
    #new_list=[x.encode('utf-8') for x in words]
    return f_list,words

def get_Data(words_list,first_list):
    try:
        chrome_options = Options()
        prefs = {'download.default_directory' : '/home/puscd/Internship/csv-project/Coding Samples/ESHA/audios'}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(url)
        html=browser.page_source
        soup=BeautifulSoup(html,"html.parser")
        #print("Soup",len(soup))
        wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/nav/div/div/ul/div[1]/button"))).click()
        print("Clicked Login")
        mail = browser.find_element_by_xpath('//*[@id="loginEmail"]')
        mail.send_keys("kalyanisvetal@gmail.com")
        print("Email Sent")
        passw = browser.find_element_by_xpath('//*[@id="loginPassword"]')
        passw.send_keys("K@lyani@11")
        print("Password Sent")
        wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div/div/form/button"))).click()

        wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='English, US']"))).click()
        wait(browser,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/section/div[1]/div/div/form/div[4]/div[1]/div[2]/div/div/div[3]/ul/li[22]/a"))).click()
        len_words=len(words_list)
        print(len_words)
        cnt=0
        for te in range(len_words):
            print("\n*** COUNT: ",cnt,"***")
            text_area = browser.find_element_by_xpath('//*[@id="main-textarea"]')
            print(words_list[te],len(words_list[te]))
            if len(words_list[te])==2:
                one_1=words_list[te][0]
                two_2=words_list[te][1]
                text_to_send=one_1+"<break time='100ms'/>"+two_2+"<break time='100ms'/>"+first_list[cnt]#+one_1+two_2
                print(text_to_send)
                cnt+=1
            elif len(words_list[te])==3:
                one_1=words_list[te][0]
                two_2=words_list[te][1]
                three_3=words_list[te][2]
                text_to_send=one_1+"<break time='100ms'/>"+two_2+"<break time='100ms'/>"+three_3+"<break time='100ms'/>"+first_list[cnt]#+one_1+two_2+three_3
                cnt+=1
                print(text_to_send)
            else:
                print("NOT AVAILABLE")
                cnt+=1
            
            text_area.send_keys(text_to_send)
            print("Sent Keys:")
            wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div[1]/div/div/form/div[4]/div[3]/div[1]/button[1]"))).click()
            print("Clicked on Convert To Speech")
            wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div[1]/div/div/form/div[3]/div/button[1]"))).click()
            print("Clicked on DOWNLOAD MP3")
            time.sleep(4)
            d_path="/home/puscd/Internship/csv-project/Coding Samples/ESHA/audios"

            f_name=latest_download_file(d_path)
            os.chdir(d_path)
            rename_name=first_list[te-1]+".mp3"
            print("Before",f_name)
            print(rename_name,len(rename_name))
            os.rename(f_name,rename_name)
            f_name=latest_download_file(d_path)
            print("After",f_name)

            text_area.clear()
    

    except TimeoutException as e:
        print(e)
        print("Timeout")
        browser.close()


def latest_download_file(path):
      os.chdir(path)
      files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
      #print(files)
      newest = files[-1]

      return newest
if __name__=="__main__":
    words,first_list=read_csv()
    get_Data(words,first_list)
    

