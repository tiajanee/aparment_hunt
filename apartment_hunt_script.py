import re
import csv
import glob
import pprint
import httplib2
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup, SoupStrainer, Tag
import os


APARTMENT_LINKS = [
"https://www.apartments.com/san-leandro-racquet-club-san-leandro-ca/64kvwjs/",
"https://www.apartments.com/amber-court-apartment-homes-fremont-ca/x4hhv4n/",
"https://www.apartments.com/the-heights-san-leandro-ca/s82z2b6/"
]

DIR = '/Users/tiaking/Desktop'

def getting_amenities():


#getting the amenities, checking for gym, pool/sauna/spa

	for i in range(len(APARTMENT_LINKS)):
		page = urlopen(APARTMENT_LINKS[i]).read()
		soup = BeautifulSoup(page, 'html')
		# print(soup)
		# soup.prettify()
		# pprint.pprint(soup)
		import json
		results = soup.find_all('div', {"class" : "col-33"})
		# print(results[0])
		
		ameneties = [result.text for result in soup('div', {"class" : "col-33"})]
		# print(ameneties)
		am_string = ""
		for i in range(len(ameneties)):
			am_string += ameneties[i]
		" ".join(am_string.split())
		# print(am_string)


		check_gym_list = ["Fitness", "Gym", "Cardio"]

		has_gym = False

		for gym in check_gym_list:
			if gym in am_string:
				has_gym = True

		check_pool_list = ["Pool", "Sauna", "Spa", "Hot Tub"]

		has_pool =  False

		for pool in check_pool_list:
			if pool in am_string:
				has_pool = True

	# print(has_gym)
	# print(has_pool)




def get_listing_attributes():
	for i in range(len(APARTMENT_LINKS)):
		page = urlopen(APARTMENT_LINKS[i]).read()
		soup = BeautifulSoup(page, 'html')
		pprint.pprint(soup)

		lease_length = [lease.text for lease in soup('li', {'class':"leaseLength"})]
		lease_string = ""
		for i in range(len(lease_length)):
			lease_string += lease_length[i]

		property_name = [name.text for name in soup('div', {'class':'propertyName'})][0]
		for character in property_name.lower():
			# print(character)
			# print(property_name.index(character))
			# no_check_list = [0,1, len(property_name), len(property_name)-1]
			# if property_name.index(character) not in no_check_list:
			# 	separator_check_one = property_name.index(character)-1
			# 	separator_check_two = property_name.index(character)+1
			if character not in 'abcdefghijklmnopqrstuvwxyz':
				new_str = property_name.replace(character, "")

		ratings = soup.find('div', class_='rating')
		title = ratings.get("title")
		# print(property_name)
		# print(new_str)
		# print(title)
	
	






get_listing_attributes()
























