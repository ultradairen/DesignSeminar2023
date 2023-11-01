# Simple Agent for Discourse with OpenAI

このプログラムは、Discourseフォーラムの議論に参加し、特定のエージェントとしての役割で返答をするシンプルなエージェントです。

## 処理の概要

1. 環境変数をロード
2. OpenAIとの設定
3. Discourseからの最新の投稿を取得
4. 最後の投稿が自分（エージェント）によるものでない場合、OpenAIのChat APIを使用して返答を生成
5. 返答をDiscourseに投稿

## 概要図
```mermaid
sequenceDiagram
    participant User as User
    participant Env as Environment Variables
    participant Discourse as Discourse Forum
    participant OpenAI as OpenAI Chat API
    participant Agent as Agent Program

    User->>Agent: Start Program
    Agent->>Env: Load environment variables
    Agent->>Discourse: Fetch latest posts
    Note over Agent: Check if latest post is by the agent
    Agent->>OpenAI: If not, send chat prompt to generate response
    OpenAI-->>Agent: Return generated response
    Agent->>Discourse: Post generated response
    Note over Agent: Wait for random interval if more iterations are left
    Agent-->>User: End program or continue loop
```
## 使用される主な環境変数

- `MAX_EXECUTION_COUNT`: エージェントの最大実行回数
- `INTERVAL_SEC_MIN`: 次回実行待ち時間の最小値（秒）
- `INTERVAL_SEC_MAX`: 次回実行待ち時間の最大値（秒）
- `DISCOURSE_LATEST_POSTS_COUNT`: Discourseから取得する過去の投稿数
- `DISCOURSE_URL`, `DISCOURSE_API_KEY`, `DISCOURSE_API_USERNAME`: Discourseの設定情報
- `OPENAI_API_KEY`, `OPENAI_MODEL`: OpenAIのAPIキーと使用するモデル名

# Colabでの操作方法
※もっと良いやり方あるかもしれないけどおそらくこんな感じ

## Githubレポジトリをダウンロード
慣れている方はCloneすればOK。

- https://github.com/ultradairen/DesignSeminar2023
- `Code` - `Download ZIP`
- どこかに解凍しておく

## .envファイル準備
.env.exampleを元に、.envファイルを作成

| 名前 | 説明 |
| -- | -- |
| MAX_EXECUTION_COUNT | 何回繰り返し実行するか設定します |
| INTERVAL_SEC_MIN | 最小実行間隔（秒）を設定します |
| INTERVAL_SEC_MAX | 最大実行間隔（秒）を設定します |
| DISCOURSE_URL | DiscourseのURLを設定します |
| DISCOURSE_API_KEY | DiscourseのAPIキーを設定します |
| DISCOURSE_API_USERNAME | DiscourseのAPIユーザー名を設定します |
| DISCOURSE_LATEST_POSTS_COUNT | 取得する直近投稿数を設定します。多くするとChatGPT処理に失敗する場合があります。|
| DISCOURSE_CATEGORY_ID | DiscourseのカテゴリIDを設定します |
| DISCOURSE_TOPIC_ID | DiscourseのトピックIDを設定します |
| OPENAI_API_KEY | OpenAIのAPIキーを設定します |
| OPENAI_MODEL | 	使用するOpenAIのモデルを設定します |

## debate_ai.ipynbをColabで開く
- https://colab.research.google.com
- `ファイル` - `ノートブックを開く`
- `GitHub`
    -  GitHub URL
      - https://github.com/ultradairen/DesignSeminar2023
    - パス
      - `debate_ai.ipynb`をクリック

## 必要ファイルのアップロード
- 左ペイン - `ファイル`クリック
- `セッションストレージにアップロード`クリック
- 以下3ファイルをアップロード
  - .env
  - requirements.txt
  - simpledcapi.py

## ペルソナ選択＆味付け
以下を変更する。`additional_instruction`はsystem promptで渡しているが、あまり影響しないかも。

```python
agent_name = "クマ - ブロンコ"
additional_instruction = """
冬眠の時期が近づいてきたので、ちょっと眠いことや、冬眠に関する意見を必ず述べてください。
"""
```

## 実行
上から順繰りに実行

## .envを変更したとき
実行回数など.envに変更を加えた場合、再アップロードとともにランタイムの再起動が必要。`ランタイム` - `ランタイムを再起動`から可能。
