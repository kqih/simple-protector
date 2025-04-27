# Discord Webhook Protector API 🚀

[![Flask](https://img.shields.io/badge/Flask-2.3+-blue)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📜 Description

A lightweight Flask-based API designed to **protect Discord webhooks from deletion**.  
Instead of exposing the original webhook URL, this API issues a unique ID for each webhook.  
You can send messages using the ID without ever revealing the real webhook URL!

The webhooks are **persistently stored** in a local `webhooks.json` file, making the system survive restarts or crashes.

---

## ✨ Features

- 🔒 Protects Discord webhook URLs by replacing them with random UUIDs
- 💾 Saves webhooks persistently into `webhooks.json`
- ⚡ Quickly add, list, and send messages through stored webhooks
- 🛡️ Handles invalid webhooks, errors, and ensures basic API stability

---

## ⚙️ Requirements

- Python 3.7+
- `Flask`
- `requests`

Install dependencies:

```bash
pip install Flask requests
```

---

## 🚀 Running the Server

```bash
python app.py
```

The server will start at:

```
http://0.0.0.0:5200
```

---

## 🛠️ API Endpoints

### ➕ Add a Webhook

**POST /add**

**Description:**  
Adds and validates a Discord webhook, returns a unique ID.

**Request Body:**

```json
{
  "webhook": "https://discord.com/api/webhooks/..."
}
```

**Responses:**

- `200 OK` — Successfully added
- `400 Bad Request` — Invalid input or invalid webhook URL

---

### 📃 List Stored Webhooks

**GET /list**

**Description:**  
Returns all stored webhooks and their associated UUIDs.

**Response:**

```json
{
  "uuid1": "https://discord.com/api/webhooks/...",
  "uuid2": "https://discord.com/api/webhooks/..."
}
```

---

### 📤 Send Message to a Webhook

**POST /<id>**

**Description:**  
Sends a JSON payload to the Discord webhook corresponding to the given UUID.

**URL Parameter:**

- `id` — Unique webhook ID

**Request Body:**

Example:

```json
{
  "content": "Hello from the protected API!"
}
```

**Responses:**

- `200 OK` — Message sent successfully
- `400 Bad Request` — Invalid ID, missing data, or bad payload
- `404 Not Found` — Webhook no longer exists
- `502 Bad Gateway` — Received non-JSON response

---

## 📂 Webhooks Storage (`webhooks.json`)

All webhooks are saved to a file called `webhooks.json` automatically.  
If the file is missing or corrupted, it will reset cleanly.

Example:

```json
{
  "9c1c4d1a-9282-4d8b-91a2-493c13a63c07": "https://discord.com/api/webhooks/xxx/yyy"
}
```

---

## 🧠 Why Protect Webhooks?

- Hide the real Discord webhook URLs from end users.
- Prevent malicious users from deleting, spamming, or misusing your webhooks.
- Add a simple control layer between your systems and Discord.

---

## 🧪 Example Usage with `curl`

**Add a webhook:**

```bash
curl -X POST http://localhost:5200/add -H "Content-Type: application/json" -d '{"webhook":"https://discord.com/api/webhooks/xxx/yyy"}'
```

**List all webhooks:**

```bash
curl http://localhost:5200/list
```

**Send data to a webhook by ID:**

```bash
curl -X POST http://localhost:5200/<uuid> -H "Content-Type: application/json" -d '{"content":"Protected message!"}'
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 💬 Final Notes

> This API is designed to **improve webhook security**, not replace Discord's native security mechanisms.  
> Always keep your API server protected and avoid exposing `webhooks.json` publicly!

