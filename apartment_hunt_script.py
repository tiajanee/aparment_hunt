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
"https://www.apartments.com/the-heights-san-leandro-ca/s82z2b6/",
"https://www.apartments.com/creekwood-hayward-ca/per3r3t/"
]

DIR = '/Users/tiaking/Desktop/apartment_hunt/apartment_listings.csv'

def main():
	for apartment in APARTMENT_LINKS:
		listing_info = get_listing_attributes(apartment)
		extras = getting_amenities(apartment)
		# create_apartment_dataset(listing_info, extras)


def getting_amenities(apartment):


#getting the amenities, checking for gym, pool/sauna/spa

	page = urlopen(apartment).read()
	soup = BeautifulSoup(page, 'html')
	
	ameneties = ([result.text for result in soup('div', {"class" : "col-33"})][0].strip() + "\n"
		+ [result.text for result in soup('div', {"class" : "col-33"})][1].strip())
	# print(ameneties)


	check_gym_list = ["Fitness", "Gym", "Cardio"]

	has_gym = False

	for gym in check_gym_list:
		if gym in ameneties:
			print(gym)
			has_gym = True

	check_pool_list = ["Pool", "Sauna", "Spa", "Hot Tub"]

	has_pool =  False

	for pool in check_pool_list:
		if pool in ameneties:
			print(pool)
			has_pool = True

	# print(has_gym)
	# print(has_pool)
	return ameneties



def get_listing_attributes(apartment):
	page = urlopen(apartment).read()
	soup = BeautifulSoup(page, 'html')
	# pprint.pprint(soup)

	lease_length = [lease.text for lease in soup('li', {'class':"leaseLength"})][0].strip()
	
	property_name = [name.text for name in soup('div', {'class':'propertyName'})][0].strip()

	rating = soup.find('div', class_='rating').get("title")
	address = [location.text for location in soup('span', {'itemprop': 'streetAddress'})][0]
	city = [city.text for city in soup('span', {'itemprop': 'addressLocality'})][0] 
	phone_number = [number.text for number in soup('span', {'class': 'phoneNumber'})][0].strip()

	deposit = [money.text for money in soup('td', {'class': 'deposit'})][0]

	size = [feet.text for feet in soup('td', {'class': 'sqft'})][0]

	rent_range = [rent.text for rent in soup.find_all('div', {'class': 'rentRollupContainer'})][0].split()[-1].strip()
	application_fee = [fee.text for fee in soup('div', {'class':'oneTimeFees'})][0].split()[3]
	
	listing = [property_name, 
	address, city, rating, phone_number, lease_length, deposit, size, rent_range, application_fee]

	return listing

def create_apartment_dataset(listing, ameneties):
	file_path = DIR

	if not os.path.exists(os.path.dirname(file_path)):
			try:
				os.makedirs(os.path.dirname(file_path))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
	
	with open(file_path, 'a') as csvfile:
		filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
		if os.path.getsize(file_path) == 0:
			filewriter.writerow(['name','address', 'city', 'rating', 'phone #', 'lease length', 'deposit',
				'size', 'rent $', "app fee", "ameneties"])

		print(listing)
		print(ameneties)
		listing.append(ameneties)
		print(listing)
		filewriter.writerow(listing)



if __name__ == "__main__":
    main()


















