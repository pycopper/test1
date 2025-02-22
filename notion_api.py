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

# ルートエンドポイント（動作確認用）
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Notion API is running!"})

# Notionにタスクを追加
@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    notion_payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": data["task_name"]}}]},
            "Status": {"select": {"name": data.get("status", "To Do")}}
        }
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=notion_payload)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
