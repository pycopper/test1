from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 環境変数からNotion API情報を取得
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json

    # **受け取るJSONデータのキーを適切に変更**
    task_name = data.get("task_name")  # Postmanから "task_name" で送信
    tag_name = data.get("tag")  # "タグ" に対応する値

    # **Notionのプロパティ名を適切に変更**
    notion_payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "名前": {"title": [{"text": {"content": task_name}}]},  # 日本語カラム
            "タグ": {"select": {"name": tag_name}} if tag_name else None
        }
    }

    # **"タグ" が None なら削除**
    notion_payload["properties"] = {k: v for k, v in notion_payload["properties"].items() if v is not None}

    response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=notion_payload)
    
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
