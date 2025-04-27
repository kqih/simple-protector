# Discord Webhook Manager API

A simple Flask-based API for managing and sending messages to Discord webhooks.

## Features

- Add and validate Discord webhooks
- List all added webhooks
- Send JSON payloads to stored webhooks via their generated ID

## Requirements

- Python 3.7+
- `Flask`
- `requests`

Install dependencies:

```bash
pip install Flask requests
```

## Running the Server

```bash
python app.py
```

The server will start on `http://0.0.0.0:5200`.

## API Endpoints

### 1. Add a Webhook

**Endpoint:**  
`POST /add`

**Description:**  
Adds a valid Discord webhook URL and returns a unique ID for it.

**Request Body:**

```json
{
  "webhook": "https://discord.com/api/webhooks/..."
}
```

**Responses:**

- `200 OK`  
  ```json
  {
    "id": "generated-uuid"
  }
  ```
- `400 Bad Request`  
  Invalid data or invalid webhook URL.

---

### 2. List All Webhooks

**Endpoint:**  
`GET /list`

**Description:**  
Returns a list of all stored webhook IDs and their associated URLs.

**Response:**

- `200 OK`  
  ```json
  {
    "id1": "https://discord.com/api/webhooks/...",
    "id2": "https://discord.com/api/webhooks/..."
  }
  ```

---

### 3. Send Data to a Webhook

**Endpoint:**  
`POST /<id>`

**Description:**  
Sends a JSON payload to the Discord webhook associated with the given ID.

**URL Parameter:**

- `id` - The unique ID of the stored webhook.

**Request Body:** (Your payload for the Discord webhook)

Example:

```json
{
  "content": "Hello from API!"
}
```

**Responses:**

- `200 OK`  
  Successfully forwarded the request. Returns Discord's webhook response.
- `400 Bad Request`  
  - Invalid ID
  - No data received
  - Error in webhook data
- `404 Not Found`  
  Webhook does not exist

---

## Notes

- Webhooks are **validated** before being stored by making a simple `GET` request to ensure they exist and belong to Discord.
- The server does **not** persist webhooks between restarts — all webhook IDs and URLs are stored in memory only.

---

## Example Usage with `curl`

**Add a webhook:**

```bash
curl -X POST http://localhost:5200/add -H "Content-Type: application/json" -d '{"webhook":"https://discord.com/api/webhooks/xxx/yyy"}'
```

**List webhooks:**

```bash
curl http://localhost:5200/list
```

**Send data to a webhook by ID:**

```bash
curl -X POST http://localhost:5200/<id> -H "Content-Type: application/json" -d '{"content":"Hello from the server!"}'
```

---

## License

This project is licensed under the MIT License.
