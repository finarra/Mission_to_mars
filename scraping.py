#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #set up splinter initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    
   
    #Run all scraping functions and store results in dectionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "facts": mars_facts(),
        "featured_image": featured_image(browser),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    #Stop webdriver and return data
    browser.quit()
    return data
 

def mars_news(browser):

    #Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    #Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #convert the browser html to a soup object and then quit the browser
    html=browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        #slide_elem.find('div', class_='content_title')

        #Use the parent element to find the firsr 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        

        #Use the parent elemento to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images
#Visit URL

def featured_image(browser):
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:

        #find the realtive image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    
    # Use the base url to create an absolute url
    img_url = url + img_url_rel

    return img_url
    

#Mars facts
def mars_facts():
#Add try/except for error handling
    try:
        #use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    #Assign coliumns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

#Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes = "table table-striped")

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())

def mars_hemispheres(browser):
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemisphere_image_urls = []
    for i in range(0,4):
        full_hem_element = browser.find_by_tag('h3')[i].click()
        hemi_html = browser.html
        hemi_soup = soup(hemi_html, 'html.parser')
        hemi_url = hemi_soup.find('img', class_='wide-image').get('src')
        hemi_full_url = url + hemi_url
        hemi_title = hemi_soup.find('h2', class_='title').text
        hemi_dict = {'img_url': hemi_full_url, 'title': hemi_title}
        hemisphere_image_urls.append(hemi_dict)
        browser.back()
    return hemisphere_image_urls





