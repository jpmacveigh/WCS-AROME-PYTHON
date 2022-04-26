import json
import requests

# Example of a Python implementation for a continuous authentication client.
# It's necessary to :
# - update APPLICATION_ID
# - update request_url at the end of the script
# unique application id : you can find this in the curl's command to generate jwt token or with Base64(consumer-key:consumer-secret) keys application
APPLICATION_ID = 'Zk8zYURrVjB5QkdBM0Y4ZjlaYkd3M0xob3IwYTpSUU52R0NIMWZUdktNOGt5R1lXYURYcjROUDhh'
# url to obtain acces token
TOKEN_URL = "https://portail-api.meteofrance.fr/private/nativeAPIs/token"
class Client_APIM_MF (object):
    '''
    Client fourni par MF pour renouveler régulièrement le token d'acces à l'API WCS.
    Cette procédure est obligatoire depuis le 12 janvier 2022.
    Voir mail de Cédric Legal (MF/DP/Services) du 11 mars 2021 qui explique comment obtenir
    la valeur de APPLICATION_ID ci-dessus.
    voir "https://portail-api.meteofrance.fr/devportal/apis"
    et "https://portail-api.meteofrance.fr/authenticationendpoint/aide_fr.do"
    pour le code Python de ce client. 
    '''
    def __init__(self):
        self.session = requests.Session()
    def request(self, method, url, **kwargs):
        # First request will always need to obtain a token first
        if 'Authorization' not in self.session.headers:
            self.obtain_token()
        # Optimistically attempt to dispatch reqest
        response = self.session.request(method, url, **kwargs)
        if self.token_has_expired(response):
            # We got an 'Access token expired' response => refresh token
            self.obtain_token()
            # Re-dispatch the request that previously failed
            response = self.session.request(method, url, **kwargs)
        return response
    def token_has_expired(self, response):
        status = response.status_code
        content_type = response.headers['Content-Type']
        if status == 401 and 'application/json' in content_type:
            if 'expired' in response.headers['WWW-Authenticate']:
                return True
        return False
    def obtain_token(self):
        # Obtain new token
        data = {'grant_type': 'client_credentials'}
        headers = {'Authorization': 'Basic ' + APPLICATION_ID}
        access_token_response = requests.post(TOKEN_URL, data=data, verify=True, allow_redirects=False, headers=headers)
        #print (access_token_response.json())
        token = access_token_response.json()['access_token']
        # Update session with fresh token
        self.session.headers.update({'Authorization': 'Bearer %s' % token})
"""        
def main():
    client = Client_APIM_MF()
    # Issue a series of API requests an example. For use this test, you must first subscribe to the arome api with your application
    client.session.headers.update({'Accept': 'application/json'})
    for i in range(1):
        response = client.request('GET', 'https://public-api.meteofrance.fr/public/arome/1.0/wms/MF-NWP-HIGHRES-AROME-001-FRANCE-WMS/GetCapabilities?service=WMS&version=1.3.0', verify=False)
        print(response.status_code)
        print (response.content)
        time.sleep(5)
if __name__ == '__main__':
    main()
"""