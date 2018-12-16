# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser

# Windows Paths
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# Function 1: Mars News
def MarsNews():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Create BeautifulSoup object; parse
    soup= bs(browser.html, 'html.parser')

    # Extract title text
    title = soup.title.text
    print(title)

    #NASA Mars News
    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

    results = soup.find("div", class_='list_text')
    news_title = results.find("div", class_="content_title").text
    news_p = results.find("div", class_ ="article_teaser_body").text
    #print(f"news_title = {news_title}")
    #print(f"news_p = {news_p}")

    mars_latest_news = [news_title, news_p]
    return mars_latest_news

# JPL Mars Space Images - Featured Image
# Function 2: JPL Image
def JPLImage():
    # Visit the url for JPL Featured Space Image here.
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Retrieve page
    browser.visit(url2)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(browser.html, 'lxml')

    # Make sure to find the image url to the full size .jpg image.
    jpl_results = soup.find('div', class_='carousel_items')
    #print(jpl_results)

    article = jpl_results.article['style']
    #print(article)

    start = article.find("url('")
    end = article.find("');")
    url_append = article[start+len("url('"):end]
    #print(url_append)

    url2_trim = url2[:24]
    #print(f"url trimmed = {url2_trim}")

    # Make sure to save a complete url string for this image.
    featured_img_url = url2_trim + url_append
    #print(featured_img_url)

    return featured_img_url

# Mars Weather
# Function 3: Mars Weather Twitter
def MarsTwitter():
    #Visit the Mars Weather twitter account here 
    url3 = "https://twitter.com/marswxreport?lang=en"

    # Retrieve page
    browser.visit(url3)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(browser.html, 'lxml')

    # Scrape the latest Mars weather tweet from the page.
    tweet_results = soup.find('li', class_ = "js-stream-item")
    #print(tweet_results)

    # Save the tweet text for the weather report as a variable called mars_weather.
    mars_weather = tweet_results.p.text
    #print(mars_weather)

    return mars_weather

# Mars Facts
# Function 4: Mars Facts
def MarsFacts():
    #Visit the Mars Facts webpage here 
    url4 = "https://space-facts.com/mars/"

    # Retrieve page
    browser.visit(url4)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(browser.html, 'lxml')

    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    tables = pd.read_html(url4)
    tables
    df = tables[0]
    df.columns = ['Parameters','Values']
    print(df)

    #Use Pandas to convert the data to a HTML table string.
    html_string = df.to_html()
    #print(html_string)

    return html_string

# Mars Hemispheres
# Function 5: Mars Hemispheres
def MarsHemispheres():
    #Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    base_url = "https://astrogeology.usgs.gov"
    img_url = []
    hemisphere_image_urls = []

    # Retrieve page
    browser.visit(url5)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(browser.html, 'lxml')

    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
    hemispheres_results = soup.find_all('div',class_ = 'item')
    for result in hemispheres_results:
        img_url.append(base_url + result.a['href'])

    # Use a Python dictionary to store the data using the keys img_url and title.
    for url in img_url:
        browser.visit(url)
        soup= bs(browser.html,'lxml')
        
        final_url_result = soup.find('div',class_ = 'downloads')
        current_url = final_url_result.ul.li.a['href']
        
        title_result = soup.find('div',class_ = 'content')
        current_title = title_result.section.h2.text
        
        hemisphere_image_urls.append({"title": current_title, "img_url": current_url})
        
    #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    #print(hemisphere_image_urls)
    return hemisphere_image_urls

# Define function to return the final list
def scrape():
    final_dict = {}
    # Return final dict in end
    #final_dict['news_title'] = MarsNews()
    #for item in MarsNews():
    marsnewsdetails = MarsNews()
    final_dict['news_title'] = marsnewsdetails[0]
    final_dict['news'] = marsnewsdetails[1]
    final_dict['featured_image'] = JPLImage()
    final_dict['mars_weather'] = MarsTwitter()
    final_dict['mars_facts'] = MarsFacts()
    #hemispheres = MarsHemispheres()
    #final_dict['hemispheres'] = []
    #for hemisphere in hemispheres:
    #    final_dict['hemispheres'].append(hemisphere)
    #return final_dict
    final_dict['mars_hemispheres'] = MarsHemispheres()
    return final_dict