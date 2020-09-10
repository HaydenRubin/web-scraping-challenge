from bs4 import BeautifulSoup as bs
import os
import requests
import pymongo
from splinter import Browser
import selenium # this does what? Selenium 3.14 is more recent than 3.5. 
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    
    # Title and paragraphs
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find_all("div", class_ = 'content_title')[1].text
    print(news_title)

    news_paragraph = soup.find_all("div", class_='article_teaser_body')[0].text
    print(news_paragraph)


    # Featured image part
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, "html.parser")

    soup_image = soup.find("img", class_ ='main_image')

    featured_image_url = f"https://www.jpl.nasa.gov/{soup_image.get('src')}"

    print(featured_image_url)


    # Table facts
    url4 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url4)
    tables

    df = tables[0]
    df.columns = ['Column 1', 'Column 2']

    df.head()

    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('Mars Facts Table.html')

    # Hemispheres
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url5)

    html = browser.html
    soup = bs(html, "html.parser")

    div_items = soup.find_all("div", class_ = 'item')
    div_items

    hemisphere_img_urls =  []

    for item in div_items:
        title = item.find('h3').text 
        browser.click_link_by_partial_text(title)
        sample = browser.find_link_by_partial_text("Sample")
        html = browser.html
        soup = bs(html, "html.parser")

        hemi_url = sample[0]["href"]

        browser.back()
        
        valles_dict = {"title": title, "img_url": hemi_url}
        
        hemisphere_img_urls.append(valles_dict)

    hemisphere_img_urls

    mars_data = {"News Title": news_title, 
    "News Paragraph": news_paragraph, 
    "Featured Image": featured_image_url, 
    "Mars Table Facts": df, 
    "Hemisphere_Image_URLs": hemisphere_img_urls}

    browser.quit()

    return mars_data