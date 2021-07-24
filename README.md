# はじめに
ブロックチェーンの学習、ポートフォリオをかねて開発,記事を書きました。
エンジニアですが、いつもマニュアル、ドキュメントはほぼ丸投げで
Qiitaの記事も初めてで見にくいところがございましたら、ご了承くださいませ。
LINEのAPIをよく利用させていただいており、LINEブロックチェーンについて少しでも理解していただけると幸いです。


### 本記事について
###### 対象者
初学者、ブロックチェーンの学習をどこから初めていいかわからない方
LINEのブロックチェーンを利用し始める技術者の方

###### 技術
AWS、Docker、Ptyhon、LINE API 、etc...


###### 環境
テストネットのみのリリースになります。
本番ネットワークは申請が必要になります。


######　参考サイト
- [FinTech Jjournal](https://www.sbbit.jp/article/fj/60992)
- [Blockchain　Biz](https://gaiax-blockchain.com/side-chain)
- [LINE Blockchain Docs](https://docs-blockchain.line.biz/ja/overview/)
- [今回作成したGitHub](https://github.com/monk-developper/portfolio)





# 目次
- チュートリアルのゴール
- LINE BlockChainの構造
- LINE BlockChainのサービスの作成
- APIの実装、構造

# チュートリアルのゴール
![output.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1729720/efc4a18a-533c-c2c2-5f1e-034ad217719a.gif)

LINEでブロックチェーンを操作できるようにしたいと思いフロントはLINEMessageで構築しました。
MessageのAPIを利用したことある方であればとても簡単な構成になっています。
テストネットのみのリリースになりますので、テストユーザーへのトークンの送信。
テストユーザーへのNFTの送信になります。



# LINE　BlockChainチュートリアル
- サービスを作成する
- Non-fungibleアイテムトークンを作成する

までがLINEのチュートリアルの内容です。
追加分が

- トークンを送信してみよう
- NFTを送信してみよう


# LINE BlockChainの構造

## 概要
簡単なLINEDveloppersの構造の紹介
![Untitled Diagram.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1729720/412b8f24-7143-8eae-b37c-28946457835f.jpeg)

##### サイドチェーン
サイドチェーンは親チェーンでトランザクションを作成し、子チェーンで相対するトランザクションを作成し、資産を転送するという手法を取ります。この時SPV（Simplified Payment Verification）と呼ばれるブロックチェーンの全データをダウンロードすることなくトランザクションの検証を行うアプローチを用いています。親チェーンのコインをサイドチェーンに転送するために、親チェーンのコインを親チェーン上の特殊なOutputに送ります。それをアンロックできるのはサイドチェーン上のSPV証明のみとなっています。



##### NFT
NFTとは、「偽造不可な鑑定書・所有証明書付きのデジタルデータ」のこと。暗号資産（仮想通貨）と同じく、ブロックチェーン上で発行および取引される。従来、デジタルデータは容易にコピー・改ざんができるため、現物の宝石や絵画などのような資産価値があるとはみなされなかった。


それでは作業に行きます。

# LINE BlockChainのサービスの作成

##### チャンネルの作成
![1-0-1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1729720/6078aaca-4ea6-21c0-a67f-44b4142f5550.png)

##### サービスの作成
![1-1-1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1729720/9b8100b6-c931-fc0b-9bd3-1870f7da4b6d.png)


![1-1-2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1729720/147aae0e-7acc-3302-9d4e-11f804527973.png)

- API Secretは、サービスを作成する際に一回のみ表示され、一度発行すると再度確認することはできないため、必ずコピーして安全な場所に保管してください。
- API KeyとAPI Secretは、LINE Blockchain Developers APIを呼び出す際に使用されます。


##### Wallteの作成
![1-2-1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1729720/0bd3348c-1797-bb85-dd8b-6a206df730d2.png)
- Wallet secretは、サービスウォレットを作成する際に一回のみ表示され、一度発行すると再度確認することはできないため、必ずコピーして安全なところに保管してください。


##### トークンの作成

![1-3-1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1729720/2dd049a6-3374-05e3-9008-69b50306574e.png)

- 一度指定したowner walletは変更できません。ご注意ください。

##### NFTの作成
![2-1-1 (1).png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1729720/3ea6c0bf-61e6-033a-0829-d325062fd145.png)


これでLINEで必要な設定は終わりです。チュートリアルではCLIからのリクエストが書いているのですが、
ヘッダー情報にsignatureが必要になるため、簡単にリクエストができません。
そのため下記のようなクラスなどを用意してテストリクエストしてください。

# APIの実装、構造


```python:LineBlockChain.py

class LineBlockChain:

    server_url = env('LBDAPIEndpoint')
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


    def __createSignTarget(self, method, path, timestamp, nonce, parameters: dict = {}):
        signTarget = f'{nonce}{str(timestamp)}{method}{path}'
        if(len(parameters) > 0):
            signTarget = signTarget + "?"

        return signTarget
# NFTを送信
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

#トークンを送信
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
```

LINEのAPIになるので、開発者ファーストに作成されており、APIの利用経験者ではあればブロックチェーンの構築はサクっと可能です。
あとは自由にLINEMessageのAPIを繋げば完成です。

# 最後に
Qiitaの記事を書くのが初めてなので、こうした方がいいよとか、あればコメントください。
もっとここを教えて欲しい！ここをこうした方がいいよ！などもあればコメントください。





