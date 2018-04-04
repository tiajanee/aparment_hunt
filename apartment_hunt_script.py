import re
import csv
import pprint
import httplib2
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup, SoupStrainer, Tag
import os


#links to all the apartments I'm interested in on Apartments.com
APARTMENT_LINKS = [
"https://www.apartments.com/san-leandro-racquet-club-san-leandro-ca/64kvwjs/",
"https://www.apartments.com/amber-court-apartment-homes-fremont-ca/x4hhv4n/",
"https://www.apartments.com/the-heights-san-leandro-ca/s82z2b6/",
"https://www.apartments.com/creekwood-hayward-ca/per3r3t/",
"https://www.apartments.com/seventy-harlan-apartments-san-leandro-ca/emzmnvq/",
"https://www.apartments.com/san-leandro-racquet-club-san-leandro-ca/64kvwjs/",
"https://www.apartments.com/berkeley-apartments-berkeleyan-berkeley-ca/2s2elpb/",
"https://www.apartments.com/the-lofts-at-albert-park-san-rafael-ca/rf33y81/",
"https://www.apartments.com/summerhill-terrace-apartments-san-leandro-ca/nhc3jtn/",
"https://www.apartments.com/marina-plaza-apartments-san-leandro-ca/ztb2ycw/",
"https://www.apartments.com/woodchase-apartment-homes-san-leandro-ca/y0h5ksv/", #9
"https://www.apartments.com/northridge-pleasant-hill-ca/f4em0gs/",
"https://www.apartments.com/1038-on-second-lafayette-lafayette-ca/381k1dg/",
"https://www.apartments.com/diablo-pointe-walnut-creek-ca/vzcnd0g/",
"https://www.apartments.com/the-retreat-walnut-creek-ca/1hw8tq7/",
"https://www.apartments.com/15fifty5-walnut-creek-ca/53vtx3q/",
"https://www.apartments.com/las-ventanas-pleasanton-ca/rjw2422/",
"https://www.apartments.com/anton-hacienda-pleasanton-ca/s3mqz07/",
"https://www.apartments.com/gatewood-apartments-pleasanton-ca/bltdbkc/",
"https://www.apartments.com/avana-stoneridge-pleasanton-ca/2m6xwx9/",
"https://www.apartments.com/galloway-pleasanton-ca/jbmnl95/",
# "https://www.apartments.com/pine-grove-san-lorenzo-ca/4lyy1xl/",
"https://www.apartments.com/sofi-dublin-dublin-ca/pb7hlbt/",
"https://www.apartments.com/parc88-fremont-ca/vmwkj6d/",
# "https://www.apartments.com/metro-7785-apartments-san-leandro-ca/dqrg8tk/",
# "https://www.apartments.com/ridgecrest-apartments-hayward-ca/1ej8r47/",
"https://www.apartments.com/hurst-highland-village-hayward-ca/0gts8n1/",
"https://www.apartments.com/hillcrest-apartment-homes-hayward-ca/s2jnk44/",
"https://www.apartments.com/cinnamon-apartments-hayward-ca/1bvre25/",
"https://www.apartments.com/park-orchard-hayward-ca/mlsymzh/",
"https://www.apartments.com/creekwood-hayward-ca/per3r3t/"
]

#where the csv file is going to be created and appended to
DIR = '/Users/tiaking/Desktop/apartment_hunt/apartment_listings.csv'

#runs all the functions
def main():
	# for apartment in APARTMENT_LINKS:
	get_listing_attributes(APARTMENT_LINKS[9])
		# create_apartment_dataset(get_listing_attributes(apartment), getting_amenities(apartment))
	print(index)

def getting_amenities(apartment):

	#getting the amenities
	page = urlopen(apartment).read()
	soup = BeautifulSoup(page, 'html')

	
	ameneties = ([result.text for result in soup('div', {"class" : "col-33"})][0].strip() + [result.text for result in soup('div', {"class" : "col-33"})][1].strip())
	
	return ameneties


def get_listing_attributes(apartment):
	page = urlopen(apartment).read()
	soup = BeautifulSoup(page, 'html')
	pprint.pprint(soup)

	#extracting lease length
	if len([lease.text for lease in soup('li', {'class':"leaseLength"})]) > 0:
		dirty_lease_length = [lease.text for lease in soup('li', {'class':"leaseLength"})][0].strip()
		lease_length = dirty_lease_length.replace(",", "")
	else:
		lease_length = ""

	#extracting the property name	
	property_name = [name.text for name in soup('div', {'class':'propertyName'})][0].strip()


	#extracting rating, address, city, phone #, deposit, size and MAX rent price.
	rating = soup.find('div', class_='rating').get("title")
	address = [location.text for location in soup('span', {'itemprop': 'streetAddress'})][0]
	city = [city.text for city in soup('span', {'itemprop': 'addressLocality'})][0] 
	phone_number = [number.text for number in soup('span', {'class': 'phoneNumber'})][0].strip()

	dirty_deposit = [money.text for money in soup('td', {'class': 'deposit'})][0]
	deposit = re.sub('[^0-9]','', dirty_deposit)
	dirty_size = [feet.text for feet in soup('td', {'class': 'sqft'})][0]
	size = re.sub('[^0-9]','', dirty_size)


	dirty_rent_range = [rent.text for rent in soup.find_all('div', {'class': 'rentRollupContainer'})][0].split()[-1].strip()
	max_rent = re.sub('[^0-9]','', dirty_rent_range)
	dirty_application_fee = [fee.text for fee in soup('div', {'class':'oneTimeFees'})][0].split()[3]
	application_fee = re.sub('[^0-9]','', dirty_application_fee)

	#splitting the rent based on contribution
	taylor = 900
	tia = int(max_rent) - taylor
	
	#saving all of the elements to a list so it writes to the CSV in order 
	listing = [property_name, 
	address, city, rating, phone_number, lease_length, deposit, size, max_rent, tia, taylor, application_fee]


	return listing

def create_apartment_dataset(listing, ameneties):
	file_path = DIR

	#ensures that it doesn't make a new csv if it's already been created
	if not os.path.exists(os.path.dirname(file_path)):
			try:
				os.makedirs(os.path.dirname(file_path))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
	
	#opens a new csv file and writes the header row but only if the csv is empty
	with open(file_path, 'a') as csvfile:
		filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
		if os.path.getsize(file_path) == 0:
			filewriter.writerow(['name','address', 'city', 'rating', 'phone #', 'lease length', 'deposit',
				'size', 'rent $', "tia", "taylor", "app fee", "gym?", "pool?", "ameneties"])


		#adding personal interest columns
		check_gym_list = ["Fitness", "Gym", "Cardio"]

		has_gym = False

		for gym in check_gym_list:
			if gym in ameneties:
				has_gym = True

		check_pool_list = ["Pool", "Sauna", "Spa", "Hot Tub"]

		has_pool =  False

		for pool in check_pool_list:
			if pool in ameneties:
				has_pool = True
			

		listing.append(has_gym)
		listing.append(has_pool)
		listing.append([ameneties])
		filewriter.writerow(listing)



if __name__ == "__main__":
    main()


















