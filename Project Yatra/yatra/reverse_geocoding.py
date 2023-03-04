#packages
import requests
import json
import pandas as pd
import time



#reverse geocoder
class ReverseGeocoder:
    #base_url
    base_url='https://nominatim.openstreetmap.org/reverse'

    def fetch(self,lat,lon):
        #headers
        headers={
            'accept-language': 'en-US,en;q=0.8',
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.56'
        }

        params={
            'format':'geojson',
            'lat':lat,
            'lon':lon
        }

        #http get request
        res=requests.get(url=self.base_url,params=params,headers=headers)
        print('HTTP GET request to URL: %s | Status code: %s' % (res.url,res.status_code))


        if res.status_code==200:
            return res
        else:
            return None
        

    def parse(self,res):
        items=res['features'][0]['properties']['address']
        try:
            road= items['road']
        except:
            road= None
        try:
            suburb=items['suburb']
        except:
            suburb=None
        try:
            county=items['county']
        except:
            county=None
        return {'road':road,'suburb':suburb,'county':county}
        #print(json.dumps(res,indent=2))

    def store_result(self, dict, df,loc):
        location_list = []
        for key in dict.keys():
            if dict[key] is not None:
                location_list.append(dict[key])
        location = ','.join(location_list)
        loc.append(location)
        return loc


    
    def run(self):
        loc=[]
        #loda corinates
        df=pd.read_csv('D:\Study\Projects\Github\YATRA-backend\Yatra_backend\Project Yatra\yatra\coordinates.csv')
        for LAT,LON in zip(df.lat,df.long):
            try:
                #extract cooridinates
                lat=LAT
                lon=LON
                
                res=self.fetch(lat,lon)
                print(json.dumps(res.json()))
                ret=self.parse(res.json())
                self.store_result(ret,df,loc)
                time.sleep(2)
            except:
                pass
        df['location']=loc
        print(df)

    def get_address(self,lat,lon):
        res=self.fetch(lat,lon)
        ret=self.parse(res.json())
        location_list = []
        for key in ret.keys():
            if ret[key] is not None:
                location_list.append(ret[key])
        location = ','.join(location_list)

        return location
        


#main driver
if __name__ == '__main__':
    reverse_gecoder= ReverseGeocoder()
    reverse_gecoder.run()
    
