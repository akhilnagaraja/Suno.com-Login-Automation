import httpx
import json

async def send_song_generation_request():
    """
    Sends a song generation request using HTTPX and the session saved from the login.
    """
    # Load session state from the saved session file
    with open("session.json", "r") as f:
        session_data = json.load(f)

    # Get the access token (make sure it's not empty)
    access_token = session_data.get("access_token", "").strip()

    if not access_token:
        print("Error: Access token is missing or invalid.")
        return

    # Headers for the request
    headers = {
        "User-Agent": session_data.get("userAgent", ""),
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # API endpoint for song generation
    url = "https://suno.com/api/generate_song"  # Replace with the correct URL

    # Prepare the payload for song generation
    payload = {
        "song_request": {
            "title": "Generated Song",
            "artist": "AI Artist",
            "genre": "Pop",
            # Add any other necessary parameters based on API docs
        }
    }

    # Send the request using HTTPX
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
            song_data = response.json()  # Assuming the API returns JSON with song info
            print("Song generation successful:", song_data)
            return song_data
        except httpx.HTTPStatusError as e:
            print(f"Error generating song: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Run the function
if __name__ == "__main__":
    import asyncio
    asyncio.run(send_song_generation_request())
