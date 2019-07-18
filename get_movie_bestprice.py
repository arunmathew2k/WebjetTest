#
# Popular movie databases, cinemaworld and filmworld, allows 2 API operations;
# one returns the movies that are available and the other returns the the details of a single movie.  
# This application allow customers to get the cheapest price for movies from these two providers.
# The app gives out the best prices based on the api availability. 
#

import json
import requests
import tabulate

api_token = 'sjd1HfkjU83ksdsm3802k'
api_url_availability = 'http://webjetapitest.azurewebsites.net/api/{xworld}/movies/'
api_url_movie_details = 'http://webjetapitest.azurewebsites.net/api/{xworld}/movie/{ID}'
headers = {'x-access-token' : api_token}


#Get available movies from movieworld/cinemaworld

def get_availability_list( service_provider ):

    api_url = api_url_availability.format(xworld=service_provider)
    #print('Main api_url: ',api_url)

    response = requests.get(api_url, headers=headers)
    #print('response: ',response)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        print("%s is currently unavailable...!" %(service_provider))
        return None


#Get details of available movies
    
def get_movie_details(service_provider,ID):

    api_url = api_url_movie_details.format(xworld=service_provider,ID=ID)
    #print('Details api_url: ',api_url)

    response = requests.get(api_url, headers=headers)
    #print('response: ',response)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        print("Movie %s from %s is currently unavailable...!" %(ID,service_provider))
        return None



def main():
    
    availability_list_cinemaworld = get_availability_list(service_provider = 'cinemaworld')
    availability_list_filmworld = get_availability_list(service_provider='filmworld')
    cw_details=[]
    fw_details=[]

    #Get movie details from Cinemaworld
    if availability_list_cinemaworld is not None:
        for i in availability_list_cinemaworld['Movies']:
            cw_details.append(get_movie_details(service_provider='cinemaworld',ID=i['ID']))
        #print("cinema details",cw_details)
        
    #Get movie details from Filmworld
    if availability_list_filmworld is not None:
        for i in availability_list_filmworld['Movies']:
            fw_details.append(get_movie_details(service_provider='filmworld',ID=i['ID']))
        #print("film details",fw_details)
  

    #Get movies from Cinemaword replaced by movies cheaper at Filmworld than Cinemaworld 
    cheap_price=cw_details
    for i in cw_details:
        if i is not None:
            for j in fw_details:
                if j is not None:
                    if i['Title'] == j['Title']:
                        if i['Price'] > j['Price']:
                            cheap_price.remove(i)
                            cheap_price.append(j)
        else:
            cheap_price.remove(i)


    #Make the list complete with movies only available in Filmworld 
    for i in fw_details:
        if i is not None:
            if not any(d['Title'] == i['Title'] for d in cheap_price):
                cheap_price.append(i)

    #Print in rows
    if cheap_price is not None:
        print("Webjet Movies Best Price List: \n")
        header = cheap_price[0].keys()
        rows =  [x.values() for x in cheap_price]
        print(tabulate.tabulate(rows, header))
    else:
        print("Service temporarily unavailable. Please try again...!")


if __name__== "__main__":
  main()
