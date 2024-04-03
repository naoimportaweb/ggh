import json, requests, re, os;

class IPLocation:
    def __init__(self):
        self.url = 'https://ipinfo.io/json'
        response = requests.get( self.url );
        if response.status_code != 200:
        	print( "Status code:", response.status_code );
        	print( response.text );
        data = response.json();
        self.ip = data['ip'];
        self.org = data['org'];
        self.city = data['city'];
        self.country = data['country'];
        self.region = data['region'];

print(  requests.get('https://api.ipify.org').text  );

proxy = "http://localhost:9051"
os.environ['http_proxy'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy

print(  requests.get('https://api.ipify.org').text  );


#iplocation = IPLocation();
#p rint( 'Detalhes de sua localização:\n ')
#p rint( 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format( iplocation.ip, iplocation.region, iplocation.country, iplocation.city, iplocation.org ))