## SLACKTOKENの設定
### cm-slackapp-test内にSlack Appを作成する
作成手順は[こちら](https://zenn.dev/kou_pg_0131/articles/slack-api-post-message)を参照

#### Slack Appを作成時の注意事項:
- 作成したSlack AppのBot Token Scopesに以下を追加する
- channels:history
- channels:read
- chat:write
- users:read
