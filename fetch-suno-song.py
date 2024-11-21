import httpx


async def check_song_status(song_uuid):
    """
    Fetches the current status of the song using its UUID via the /feed API.
    """
    # API endpoint for checking song status
    url = f"https://suno.com/api/feed/{song_uuid}"  # Replace with the correct URL

    # Send GET request to fetch status
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

            # Assuming the API returns JSON with the song status info
            song_status = response.json()
            print("Song status:", song_status)

            # Handle the song status (you can modify the conditions based on your API response)
            if song_status.get("status") == "completed":
                print("Song generation completed successfully!")
            elif song_status.get("status") == "processing":
                print("Song is still being generated. Please wait...")
            elif song_status.get("status") == "failed":
                print("Song generation failed.")
            else:
                print("Unknown status received.")

        except httpx.HTTPStatusError as e:
            print(f"Error fetching song status: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# Example usage
if __name__ == "__main__":
    import asyncio

    # Use the UUID obtained from Part 2
    song_uuid = "your-song-uuid-here"  # Replace with actual song UUID
    asyncio.run(check_song_status(song_uuid))
