from flask import Flask, request, jsonify
import requests
import uuid
app = Flask(__name__)


ids = {}


def is_valid_webhook(url):
    if requests.get(url).status_code == 200 and "https://discord.com/api/webhooks" in url:
        return True
    else:
        return False

@app.route("/add", methods=["POST"])
def add_webhook():
    data = request.json

    if not data or "webhook" not in data:
        return "Invalid data", 400

    webhook_url = data["webhook"]


    if not is_valid_webhook(webhook_url):
        return "Invalid webhook URL", 400

    id = str(uuid.uuid4())
    ids[id] = webhook_url

    return jsonify({"id": id}), 200



@app.route("/list", methods=["GET"])
def list_webhooks():
    return jsonify(ids), 200


@app.route("/<id>", methods=["POST"])
def webhook(id):

    if id not in ids:
        return "Invalid ID", 400

    webhook_url = ids[id]


    data = request.json

    if not data:
        return "No webhook data received", 400
    
    


    r = requests.post(webhook_url, json=data)
    
    if r.status_code == 404:
        return "Webhook does not exist", 404
    elif r.status_code == 400:
        return "Error in webhook data", 400
    elif r.status_code != 200:
        return "Error sending webhook", r.status_code
    
    return r.json(), 200

app.run(host="0.0.0.0", port=5200)
