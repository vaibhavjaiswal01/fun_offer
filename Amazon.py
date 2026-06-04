import requests
from bs4 import BeautifulSoup

# Set the URL of the Amazon page you want to scrape
url = 'https://amzn.to/3hrzHV7'


# Make a request to the URL and get the HTML content
html = requests.get(url).text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
print(soup)

# Find the image tag with the class "a-dynamic-image"
image_tag = soup.find('img', {'class': 'a-dynamic-image'})

# Get the image URL from the "data-a-dynamic-image" attribute
image_url = image_tag['data-a-dynamic-image']

# # Find the product name element with the id "productTitle"
# product_name_element = soup.find('span', {'id': 'productTitle'})

# # Get the product name from the element text
# product_name = product_name_element.text.strip()




# Print the image URL
print(image_url)
#print(product_name)

