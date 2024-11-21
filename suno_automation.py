import asyncio
from playwright.async_api import async_playwright

async def automate_login():
    """
    Automates Suno.com login using Playwright, handles dynamic elements,
    and saves the session to a JSON file.
    """
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=False,  # Run with GUI for debugging
            args=["--disable-blink-features=AutomationControlled"]  # Avoid detection
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            ),  # Valid user agent
            viewport={"width": 1280, "height": 720},  # Set viewport size
            java_script_enabled=True  # Enable JavaScript
        )

        page = await context.new_page()

        # Navigate to Suno login page
        await page.goto("https://suno.com/login")
        print("Navigating to Suno login page...")

        # Wait for "Login with Google" button to appear and click it
        try:
            await page.wait_for_selector("text=Login with Google", timeout=60000)
            await page.click("text=Login with Google")
            print("Clicked 'Login with Google' button.")
        except Exception as e:
            print(f"Error: Unable to find or click 'Login with Google'. {e}")
            print("Waiting for user to complete Google login...")
            await page.wait_for_url("https://suno.com/", timeout=120000)
            print("Login successful! Saving session...")

            # Save session state to a JSON file for API usage
            await context.storage_state(path="session.json")
            print("Session saved as 'session.json'.")
            await browser.close()
            return

        # Wait for user to manually complete Google login
        print("Waiting for user to complete Google login...")
        try:
            await page.wait_for_url("https://suno.com/dashboard", timeout=120000)
            print("Login successful! Saving session...")
            await context.storage_state(path="session.json")  # Save session after successful login
            print("Session saved as 'session.json'.")
        except Exception as e:
            print(f"Error: Failed to navigate to the dashboard. {e}")
        finally:
            await browser.close()

# Run the login automation
if __name__ == "__main__":
    asyncio.run(automate_login())
