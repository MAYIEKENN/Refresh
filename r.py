from flask import Flask, jsonify
import asyncio
import aiohttp

app = Flask(name)

# API URLs (update these with your actual endpoints)
FETCH_URL = "https://api.xalyon.xyz/v2/atom/?endpoint=num"
SEND_URL = "https://api.xalyon.xyz/v2/refresh"

async def fetch_numbers():
    """Fetch phone numbers from the external API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(FETCH_URL) as response:
            if response.status == 200:
                return await response.json()  # Assuming the response is a JSON list
            else:
                print(f"Failed to fetch numbers. Status: {response.status}")
                return []

async def send_request(session, phone):
    """Send a request for each phone number."""
    url = f"{SEND_URL}?phone={phone}"
    async with session.get(url) as response:
        text = await response.text()
        print(f"Phone: {phone}, Status: {response.status}, Response: {text}")
        return {"phone": phone, "status": response.status, "response": text}

async def process_numbers():
    """Fetch phone numbers and process them concurrently."""
    phone_numbers = await fetch_numbers()
    if not phone_numbers:
        return {"error": "No phone numbers available."}
    
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, phone) for phone in phone_numbers]
        results = await asyncio.gather(*tasks)
    return results

@app.route("/process", methods=["GET"])
def process():
    """
    API endpoint to process phone numbers.
    This route runs the asynchronous tasks and returns the result as JSON.
    """
    results = asyncio.run(process_numbers())
    return jsonify(results)

if name == 'main':
    app.run(host="0.0.0.0", port=5000, debug=True)
