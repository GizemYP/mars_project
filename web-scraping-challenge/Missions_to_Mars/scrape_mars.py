from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

#!which chromedriver

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

#NASA NEWS
def scrape():
    browser = init_browser()
    mars = {}

    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('div', class_='list_text')

    for article in articles:
        try:
            
            news_title = article.a.text
            news_p = article.find('div',class_='article_teaser_body').text
            mars['headline'] = news_title
            mars['subtext'] = news_p
            #browser.click_link_by_partial_text('More')

        except:
            print("Scraping Complete")

    

    #NASA IMAGE
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA17449_hires.jpg'
    mars['featured_img'] = featured_image_url

    

    #NASA TWITTER
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweet = soup.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    hidden = soup.find('a',class_='twitter-timeline-link u-hidden').text
    l_break = "\n"

    mars_weather = tweet.replace(hidden,'').replace(l_break,' ')
    mars['weather'] = mars_weather
    #mars_weather

    

    #SPACE FACTS
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    tables = tables[1].to_html()
    mars['facts'] = tables
    

    #MARS HEMISPHERE IMAGES
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_link = soup.find_all('div',class_='description')
    

    wide_image_urls = []
    title = []
    img_url = []

    for link in img_link:
        try:
            description = link.h3.text
            title.append(description)
            partial_link = link.a['href']
            small_image_link = f"https://astrogeology.usgs.gov{partial_link}"
            wide_image_urls.append(small_image_link)
            for urlx in wide_image_urls:
                try:
                    browser.visit(urlx)
                    html = browser.html
                    soup = BeautifulSoup(html, 'html.parser')
                    final_image = soup.find_all('img',class_='wide-image')[0]['src']
                    img_url.append(f'https://astrogeology.usgs.gov{final_image}')
                    #print(final_image)
                    browser.visit(url5)
                except:
                    print('error')   
        except:
            print('issue')

        hemisphere_image_urls = []
        img_dict = {}

    x=0
    while x < 4:
        
        img_dict['title'] = title[x]
        img_dict['img_url'] = wide_image_urls[x]
        hemisphere_image_urls.append(dict(img_dict))
        x +=1

    mars['hemisphere'] = img_url
    mars['caption'] = title
    
    return mars