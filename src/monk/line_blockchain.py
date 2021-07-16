import os ,environ,random ,string ,requests ,hmac ,hashlib ,base64
from pprint import pprint
from monk.request_flattener import RequestBodyFlattener
BASE_DIR = environ.Path(__file__) - 2
env = environ.Env()
env_file = str(BASE_DIR.path('.env'))
env.read_env(env_file)

class LineBlockChain:

    server_url = env('LBDAPIEndpoint')
    # server_url = env('HOSTAPIEndpoint')
    service_api_key = env('APIKey')
    service_api_secret = env('APISecret')


    def getTimestamp(self):
        path = '/v1/time'
        headers = {
            'service-api-key': self.service_api_key,
        }
        res = requests.get(self.server_url + path, headers=headers)
        return res.json()['responseTime']

    def getNonce(self):
        nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        return nonce

    def getSignature(self, secret: str, method: str, path: str, timestamp: int, nonce: str, query_params: dict = {}, body: dict = {}):
        body_flattener = RequestBodyFlattener()
        all_parameters = {}
        all_parameters.update(query_params)
        all_parameters.update(body)

        signTarget = self.__createSignTarget(method.upper(), path, timestamp, nonce, all_parameters)

        if (len(query_params) > 0):
            signTarget += '&'.join('%s=%s' % (key, value) for (key, value) in query_params.items())

        if (len(body) > 0):
            if (len(query_params) > 0):
                signTarget += "&" + body_flattener.flatten(body)
            else:
                signTarget += body_flattener.flatten(body)

        raw_hmac = hmac.new(bytes(secret, 'utf-8'), bytes(signTarget, 'utf-8'), hashlib.sha512)
        result = base64.b64encode(raw_hmac.digest()).decode('utf-8')

        return result

    def getWallets(self):

        nonce = self.getNonce()
        timestamp = self.getTimestamp()

        path = '/v1/wallets'
        method = 'GET'
        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
            'signature' : self.getSignature(self.service_api_secret , method, path,timestamp, nonce)
        }
        res = requests.get(self.server_url + path, headers=headers)
        return res.json()


    def GET_v1_services_serviceId(self):

        nonce = self.getNonce()
        timestamp = self.getTimestamp()

        path = '/v1/services/'+env('SERVICEID')
        method = 'GET'
        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
            'signature' : self.getSignature(self.service_api_secret , method, path,timestamp, nonce)
        }

        res = requests.get(self.server_url + path, headers=headers)
        return res.json()

    def GET_v1_users_userId(self):

        nonce = self.getNonce()
        timestamp = self.getTimestamp()

        method = 'GET'
        path = '/v1/users/Ucdd3d08e3ff8252cb13771ae0b9363a5'

        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
            'signature' : self.getSignature(self.service_api_secret , method, path,timestamp, nonce)
        }
        res = requests.get(self.server_url + path, headers=headers)
        return res.json()

    def __createSignTarget(self, method, path, timestamp, nonce, parameters: dict = {}):
        signTarget = f'{nonce}{str(timestamp)}{method}{path}'
        if(len(parameters) > 0):
            signTarget = signTarget + "?"

        return signTarget

    def POST_v1_item_tokens_contractId_non_fungibles_tokenType_mint(self):

        nonce = self.getNonce()
        timestamp = self.getTimestamp()
        method = 'POST'

        path = '/v1/item-tokens/'+env('ItemContractID')+'/non-fungibles/'+env("NonFungibleTokenType")+'/mint'

        request_body = {
            'ownerAddress': env("WalletAddress"),
            'ownerSecret' : env("WalletSecret"),
            'name': 'monkMovieTicket',
            'toAddress': env("UserAWallet"),
        }

        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
            'Content-Type': 'application/json',
            'signature' : self.getSignature(self.service_api_secret , method, path,timestamp, nonce ,  body=request_body )
        }

        res = requests.post(self.server_url + path, headers=headers, json=request_body)
        return res.json()

    def POST_v1_wallets_walletAddress_service_tokens_contractId_transfer(self):

        nonce = self.getNonce()
        timestamp = self.getTimestamp()
        method = 'POST'

        path = '/v1/wallets/'+env("WalletAddress")+'/service-tokens/'+env("ServiceContractID")+'/transfer'

        request_body = {
            'walletSecret': env("WalletSecret"),
            'toAddress': env("UserBWallet"),
            'amount': '10000000'
        }
        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
            'Content-Type': 'application/json',
            'signature' : self.getSignature(self.service_api_secret , method, path,timestamp, nonce ,  body=request_body )
        }

        res = requests.post(self.server_url + path, headers=headers, json=request_body)
        return res.json()

    def GET_v1_item_tokens_contractId_non_fungibles(self):

        nonce = self.getNonce()
        timestamp = self.getTimestamp()

        method = 'GET'

        path = '/v1/item-tokens/'+env('ItemContractID')+'/non-fungibles'

        query_params = {
            'limit': 10,
            'orderBy': 'desc',
            'page': 1
        }
        headers = {
            'service-api-key': self.service_api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
            'signature' : self.getSignature(self.service_api_secret , method, path,timestamp, nonce ,query_params)
        }
        res = requests.get(self.server_url + path, headers=headers, params=query_params)
        return res.json()