このリポジトリは練習用に作成したアプリケーションです。

## 概要
serverless framework を用いて、Slackの指定したチャンネルから指定の単語を検索して取ってきた情報をS3に出力して、その概要をSlackの指定したチャンネルに通知するアプリケーションです。

## 準備
git cloneした後に、以下のコマンドを実行してください。

```
npm install -g serverless
npm install
```

## SLACKTOKENの設定
parameter store に secure string にて python_slack_app_token の名前でslackのapi tokenを保存する必要があります。

## Slack Appを作成する
作成手順は[こちら](https://zenn.dev/kou_pg_0131/articles/slack-api-post-message)を参照

### Slack Appを作成時の注意事項:
- 作成したSlack AppのBot Token Scopesに以下を追加する
- channels:history
- channels:read
- chat:write
- users:read

### 通知先チャンネルにSlack Appを追加する
通知先のチャンネルに作成したアプリを追加してください。


## AWS Profileの設定
各自お任せします。
権限はAdministratorAccess権限です。


## デプロイ
```
sls deploy --aws-profile <profile名>
```

## Lambdaの設定
aws lambda の環境変数より各種設定が必要です。
情報取得先のSlackチャンネルなどの情報は必須なので設定忘れのないように。
