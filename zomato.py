import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pprint
import json

##Task-1
driver = webdriver.Chrome()
driver.get("https://www.zomato.com/ncr")
page = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
soup = BeautifulSoup(page,'html.parser')

## finding the name of the localities and store it to loicalities list
main_div = soup.find('div',class_='ui segment row')
res_list = main_div.findAll('a')

json_data=[]
url_list = []
index = 1
for i in res_list:
	data = {}
	name = ''
	for j in (i.text.strip()):
		if '(' == j:
			break
		else:
			name+=j
	print(str(index)+'.', name)
	data[index]=name
## finding the number of restraunts in the given localities
	res_num = i.find('span').text[1:-1]
	print('    Total Restraunts = ', res_num)
	data['Total_Restraunts']=res_num
	json_data.append(data)
	index+=1
	print()
	url = i['href']
	url_list.append(url)


with open('Task_1.json','w') as new_file:
	json.dump(json_data,new_file)

## Task-2
user1 = int(input('select your locality for restrount list : '))

restraunt_detail = []
names = []
ids = []
localities = []
reviews = []
ratings = []
prices = []

#finding the link of see more and call , 
driver = webdriver.Chrome()
driver.get(url_list[user1-1])
page = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
soup = BeautifulSoup(page,'html.parser')
## link of see more lists------
link = soup.findAll('a',class_='zred')
for i in link:
	driver = webdriver.Chrome()
	driver.get(i['href'])
	page = driver.execute_script("return document.documentElement.outerHTML")
	driver.quit()
	soup = BeautifulSoup(page,'html.parser')

##	finding the restraunt name and the locality of the restraunt
	res_name = soup.findAll('div',class_='col-s-12')
	for x in res_name:
		name = x.findAll('a')
		names.append(name[-2].text.split('\n')[0])
#		finding the name of locality----
		localities.append(name[-1].text.strip())

##	finding the Ids of the restraunt----	
	divs =soup.findAll('div',class_='ta-right floating search_result_rating col-s-4 clearfix')
	for d in divs:
		e=d.find('div',class_='rating-popup')
		f=e.get('data-res-id')
		ids.append(f)
	
##	finding the review and the ratings of the restraunts-----
	res_rev = soup.findAll('div',class_="ta-right floating search_result_rating col-s-4 clearfix")
	for x in res_rev:
		review = x.find('span')
		if type(review) != type(None):
			reviews.append(review.text)
		else:
			reviews.append('0 votes')
#		rating------
		rating = x.find('div').text.strip()
		ratings.append(rating)

##  finding the price range of the restraunt------
	res_price = soup.findAll('div',class_='res-cost clearfix')
	for x in res_price:
		price = x.find('span',class_="col-s-11 col-m-12 pl0").text
		prices.append(price)

##  storing the dota into a dictionary and then into a list----
for index in range(len(names)):
	detail = {}
	detail['name'] = (names[index])
	detail['locality'] = (localities[index])
	detail['review'] = (reviews[index])
	detail['rating'] = (ratings[index])
	detail['price'] = (prices[index])
	detail['Id'] = ids[index]
	restraunt_detail.append(detail)

pprint.pprint(restraunt_detail)
with open('Task_2.json','w') as second_file:
	json.dump(restraunt_detail,second_file)
