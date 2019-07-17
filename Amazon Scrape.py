from bs4 import BeautifulSoup
import requests
import pandas as pd

product_no = 0
product_info = {}
# PROVIDE THE URL
url="https://www.amazon.in/Philips-Xenium-E168-Mobile-Phone-Black/product-reviews/B07J6T286Q/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

response = requests.get(url)
print(response)
data = response.text
#print(data)
soup = BeautifulSoup(data, 'html.parser')
products = soup.find_all('div', {'class': 'a-section review aok-relative'})

page_no = 1

while True:

    for product in products:
        product_review_tag = product.find('i', {'data-hook': 'review-star-rating'})
        product_review = product_review_tag.text if product_review_tag else "N/A"
        print(product_review)
        product_title = product.find('a', {'class': 'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'}).findNext('span').contents[0]
        print(product_title)
        product_name = product.find('span', {'class': 'a-size-base review-text review-text-content'}).findNext('span').contents[0]
        print(product_name)

        if product_review != "N/A":
            product_no += 1
            product_info[product_no] = [product_review, product_title, product_name]


    url_tag = soup.find('li', {'class': 'a-disabled a-last'})
    print(url_tag)
    if url_tag:
        break
    else:
        url_tag = soup.find('li', {'class': 'a-last'}).findNext('a')
        url = 'https://www.amazon.in' + url_tag.get('href')
        response = requests.get(url)
        print(response)
        data = response.text
        # print(data)
        soup = BeautifulSoup(data, 'html.parser')
        products = soup.find_all('div', {'class': 'a-section review aok-relative'})
        page_no += 1
        print('page_no:', page_no)
        print(url)

print("Total products:", product_no)

product_list = pd.DataFrame.from_dict(product_info, orient='index',
                                     columns=['Rating Star', 'Title', 'Review'])

product_list.head()

product_list.to_csv('product_list.csv',encoding='utf-8')

print('saved to - product_list.csv')
