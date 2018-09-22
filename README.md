## Contents
* **IoTテンプレートアプリ.zip**：「IoTテンプレートアプリ」のkintoneアプリテンプレートです。
* **S3ToKintone-python**：Amazon S3にストアされたSoracom IoTデータをkintoneに連携するLambdaを定義するServerless Frameworkのパッケージです。

## S3ToKintone-python
### S3に入るIoTデータ
Soracom側の送信内容をチェックします。今回のサンプルは次のようなデータを想定しています。

```:json
{
  "operatorId": "OP0030368396",
  "timestamp": 1535892789599,
  "destination": {
    "resourceUrl": "https://firehose.ap-northeast-1.amazonaws.com/doto_hackathon_team1",
    "service": "firehose",
    "provider": "aws"
  },
  "credentialsId": "doto_hackathon_team1_iam_user",
  "payloads": {
    "prsp": 101743,
    "tmpc": 27.06999969482422,
    "gatewayData": [
      {
        "date": "2018-09-02T21:53:04.743531+09:00",
        "rssi": -26,
        "snr": 11,
        "gwid": "000b78fffeb000e9",
        "channel": 923200000
      }
    ],
    "deveui": "000b78fffe050b09",
    "date": "2018-09-02T21:53:04.743531+09:00",
    "data": "5c8fd84180b7c647",
    "binaryParserEnabled": true
  },
  "sourceProtocol": "lora",
  "deviceId": "000b78fffe050b09"
}
```

これに対応するkintone連携部分は ```handler.py``` に記載があります。取得できるセンサーに応じてJSONフォーマットも変わるので、必要に応じて、次の ```Soracom``` クラスも書き換えます。

```:python
class Soracom(model.kintoneModel):
    def __init__(self, data, label=""):
        super(Soracom, self).__init__()
        self.label = label
        self.date = data['payloads']['date']
        self.deveui = data['payloads']['deveui']
        self.tmpc = data['payloads']['tmpc']
        self.prsp = data['payloads']['prsp']
```

### Serverless Frameworkを用いたLambdaのデプロイ
#### 設定値
今回はAmazon S3にストアされたSoracom IoTデータをkintoneに連携するLambdaをデプロイしますが、設定値として ```serverless.yml``` の次のパラメータをセットします。
- ```defaultBucket```: AWS IoTやkinesis firehoseを経由して送信されたIoTデータがストアされているS3バケットのバケット名
- ```defaultSubdomain```: kintoneのサブドメイン（ホスト名 ```subdomain.cybozu.com``` の ```subdomain``` 部分）
- ```defaultAppId```: kintoneアプリのID
- ```defaultApiToken```: kintoneアプリのAPIトークン

#### プリインストール
- Node.js
- Serverless Framework（ ```npm install -g serverless``` でインストール）

#### 依存ライブラリ
- ```serverless-plugin-existing-s3```（ ```npm install serverless-plugin-existing-s3``` でインストール）
- ```pykintone``` （ ```pip install pykintone -t .``` でインストール）

#### デプロイコマンド
```
sls deploy && sls s3deploy
```

## Reference
* Amazon S3に入ったSoracom IoTデータをkintoneに連携する方法 (presentation on Slideshare) [[日本語](https://www.slideshare.net/yamaryu0508b/amazon-s3soracom-iotkintone-115625500 "Amazon S3に入ったSoracom IoTデータをkintoneに連携する方法 (presentation on Slideshare)")]
* Serverless Frameworkドキュメント [[English](https://serverless.com/ "Serverless Frameworkドキュメント")]
