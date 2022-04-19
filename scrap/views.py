from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from django.shortcuts import redirect, render
from . import models
import os
# Create your views here.
"""
heroku settings...
Buildpack URL:
    https://github.com/heroku/heroku-buildpack-google-chrome
    https://github.com/heroku/heroku-buildpack-chromedriver

config vars:
    CHROMEDRIVER_PATH = /app/.chromedriver/bin/chromedriver
    GOOGLE_CHROME_BIN = /app/.apt/usr/bin/google-chrome
"""


url = 'https://medium.com/tag/{}'

#The Crawling function
def crawling(title, author, img, demo_link, official_link):
    print('crawling')
    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-shm-usage")
    driver_link = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)
    driver_link.get(demo_link)
    html_link = driver_link.page_source
    soup_link = BeautifulSoup(html_link, "html.parser")
    header = soup_link.find('header')
    details = header.find('p', {'class': 'pw-published-date'}).text + ', ' + header.find('div',{'class': 'pw-reading-time'}).text
    all = soup_link.find('section')
    para = all.find_all('p')
    sd = ''
    for p in para:
        sd += str(p.text) + '\n'
    driver_link.close()
    models.Front.objects.get_or_create(title=title, author=author, img=img, link=official_link, text=sd, details=details)


def new_search(request):
    try:
        record = models.Front.objects.all()
        record.delete()
        print("Record deleted successfully!")
    except:
        print("Record doesn't exists")

    if request.method == 'POST':
        search = request.POST.get('search').lower()
        final_url = url.format(quote_plus(search))
        # Heroku Settings....
        op =webdriver.ChromeOptions()
        op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        op.add_argument("--headless")
        op.add_argument("--no-sandbox")
        op.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)
        
        driver.get(final_url)
        response = requests.get(final_url)
        print(response.status_code)
        if response.status_code == 404:
            err = search
            return render(request, 'scrap/error.html', {'err': err})
        else:
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            all_divs = soup.find('div', {'class': 'l'})
            job_profiles = all_divs.find_all('article')

            count = 0
            for job_profile in job_profiles:
                title = job_profile.h2.text
                author = job_profile.p.text
                img = job_profile.find('img', {'class': ''})
                if img is None:
                    img = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png'
                    print('no image')
                else:
                    img = img['src']
                link = job_profile.find('div', {'class': 'l fs'})
                official_link =  'https://medium.com' + link.find('a',class_='')['href']
                print('going to crawl')
                print(title)
                crawling(title,author,img,official_link,official_link)   #crawling function
                count += 1
                if count == 3:
                    break
            return redirect('results')
    return render(request, 'scrap/new_search.html')


def results(request):
    front = models.Front.objects.all()
    return render(request, 'scrap/results.html', {'front': front})

def details(request,pk):
    front = models.Front.objects.all().filter(id=pk)
    return render(request, 'scrap/details.html', {'front': front})

