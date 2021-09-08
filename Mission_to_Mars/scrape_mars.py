import pandas as pd 
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape():

	# Set Executable Path
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=False)


	# Scrape NASA Mars News Data
	mars_news_url = 'https://redplanetscience.com/'

	browser.visit(mars_news_url)
	time.sleep(2)

	html = browser.html
	soup = bs(html, 'html.parser')

	news_title = soup.find('div', class_='content_title').text
	news_p = soup.find('div', class_='article_teaser_body').text



	# Scrape JPL Mars Space Images

	space_images_url = 'https://spaceimages-mars.com/'

	html = browser.html
	soup = bs(html, 'html.parser')

	browser.visit(space_images_url)
	time.sleep(2)

	browser.links.find_by_partial_text('FULL IMAGE').click()

	feature_img_html = browser.html
	soup = bs(feature_img_html, 'html.parser')

	relative_image_path = soup.find('img', class_='fancybox-image')['src']
	feature_img = space_images_url + relative_image_path


	# Scrape Mars Facts Data

	mars_facts_url = 'https://galaxyfacts-mars.com/'

	facts_df = pd.read_html(mars_facts_url, header=0)[0]
	facts_df.set_index('Mars - Earth Comparison', inplace=True)
	facts_html = facts_df.to_html()

	#####Format Table: Center Align Header and Add Striped Rows
	
	facts_html = facts_html.replace('right','center')
	facts_html = facts_html.replace('dataframe','table table-striped')


	# Scrape Mars Hemispheres Data

	astrogeology_url = 'https://marshemispheres.com/'

	browser.visit(astrogeology_url)
	time.sleep(2)

	html = browser.html
	soup = bs(html, 'html.parser')

	results = soup.find_all('h3')[0:-1]

	image_urls = []

	for result in results:
	    titles = result.text
	    browser.links.find_by_partial_text(titles).click()
	    
	    html2 = browser.html
	    soup2 = bs(html2, 'html.parser')
	    
	    title = soup2.find('h2', class_='title').text
	    title = title.replace("Enhanced","").strip()
	    
	    sample = soup2.find('li')
	    imgurl = sample.find('a')['href']
	    imgurl = astrogeology_url + imgurl
	    
	    hemisphere_dict = {"title" : title, "img_url" : imgurl}
	    image_urls.append(hemisphere_dict)
	    
	    browser.links.find_by_partial_text('Back').click()
	
	# Create Dictionary for all scraped data
	scrape_data = {
		"news_title":news_title,
		"news_paragraph":news_p,
		"feature_image":feature_img,
		"mars_facts":facts_html,
		"hemispheres":image_urls
	}

	# Close Browser
	browser.quit()

	# Return Data
	return scrape_data



