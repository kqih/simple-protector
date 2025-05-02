from flask import Flask, request, jsonify
import requests
import uuid
import json
import os

app = Flask(__name__)

WEBHOOKS_FILE = "webhooks.json"

def load_webhooks():
    if os.path.exists(WEBHOOKS_FILE):
        with open(WEBHOOKS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_webhooks(ids):
    with open(WEBHOOKS_FILE, "w") as f:
        json.dump(ids, f, indent=4)

def is_valid_webhook(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200 and "https://discord.com/api/webhooks" in url
    except requests.RequestException:
        return False

@app.route("/add", methods=["POST"])
def add_webhook():
    data = request.get_json()

    if not data or "webhook" not in data:
        return "Invalid data", 400

    webhook_url = data["webhook"]

    if not is_valid_webhook(webhook_url):
        return "Invalid webhook URL", 400

    ids = load_webhooks()
    webhook_id = str(uuid.uuid4())
    ids[webhook_id] = webhook_url
    save_webhooks(ids)

    return jsonify({"id": webhook_id}), 200


@app.route("/<id>", methods=["POST"])
def webhook(id):
    ids = load_webhooks()

    if id not in ids:
        return "Invalid ID", 400

    webhook_url = ids[id]
    data = request.get_json()

    if not data:
        return "No webhook data received", 400

    try:
        r = requests.post(webhook_url, json=data, timeout=5)
    except requests.RequestException:
        return "Failed to send webhook", 500

    if r.status_code == 404:
        return "Webhook does not exist", 404
    elif r.status_code == 400:
        return "Error in webhook data", 400
    elif r.status_code != 200:
        return "Error sending webhook", r.status_code

    try:
        return r.json(), 200
    except ValueError:
        return "Received non-JSON response", 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200)
