## 準備
git cloneした後に、以下のコマンドを実行してください。

```
npm install -g serverless
npm install
```

## SLACKTOKENの設定
### Slack Appを作成する
作成手順は[こちら](https://zenn.dev/kou_pg_0131/articles/slack-api-post-message)を参照

#### Slack Appを作成時の注意事項:
- 作成したSlack AppのBot Token Scopesに以下を追加する
- channels:history
- channels:read
- chat:write
- users:read

#### 通知先チャンネルにSlack Appを追加する
通知先のチャンネルに作成したアプリを追加してください。


### AWS Profileの設定
各自お任せします。
権限はAdministratorAccess権限です。


## デプロイ
```
sls deploy --aws-profile <profile名>
```
