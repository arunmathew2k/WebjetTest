import json
import requests

api_token = 'sjd1HfkjU83ksdsm3802k'
api_url_availability = 'http://webjetapitest.azurewebsites.net/api/{xworld}/movies/'
api_url_movie_details = 'http://webjetapitest.azurewebsites.net/api/{xworld}/movie/{iD}'
headers = {'x-access-token' : api_token}


#Get available movies from movieworld/cinemaworld

def get_availability_list( service_provider ):

    api_url = api_url_availability.format(xworld=service_provider)
    print('api_url: ',api_url)

    response = requests.get(api_url, headers=headers)
    print('response: ',response)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


#Get details of available movies
    
def get_movie_details(service_provider,iD):

    api_url = api_url_movie_details.format(xworld=service_provider,iD=iD)
    print('api_url: ',api_url)

    response = requests.get(api_url, headers=headers)
    print('response: ',response)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None



def main():
    
    availability_list_cinemaworld = get_availability_list(service_provider = "cinemaworld")
    availability_list_filmworld = get_availability_list(service_provider="filmworld")
    #print("availability_list_cinemaworld: ",availability_list_cinemaworld['Movies'])
    
    if availability_list_cinemaworld is not None:
        cw_details=[]
        for i in availability_list_cinemaworld['Movies']:
            cw_details.append(get_movie_details(service_provider="cinemaworld",iD=i['ID']))            
        #print("cinema details",cw_details)

    if availability_list_filmworld is not None:
        fw_details=[]
        for i in availability_list_filmworld['Movies']:
            fw_details.append(get_movie_details(service_provider="filmworld",iD=i['ID']))            
        #print("film details",fw_details)

    cheap_price=cw_details
    for i in cw_details:
        for j in fw_details:
            if i["Title"] == j["Title"]:
                if i["Price"] > j["Price"]:
                    cheap_price.remove(i)
                    cheap_price.append(j)
        
    print("Cheap Movie: ", cheap_price)


if __name__== "__main__":
  main()
