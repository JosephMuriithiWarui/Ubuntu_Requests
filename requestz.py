import requests
import os
from urllib.parse import urlparse
import hashlib

def fetch_image(url):
    """Fetch and save an image from a URL into the Fetched_Images folder."""
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)

        # Fetch the image
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()  # Raise exception for bad status codes

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        if not filename:  # If URL doesn’t end with a file
            filename = "downloaded_image.jpg"

        # Prevent duplicate downloads by using a hash of the content
        file_hash = hashlib.md5(response.content).hexdigest()[:10]
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{file_hash}{ext if ext else '.jpg'}"

        filepath = os.path.join("Fetched_Images", filename)

        # Save image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP error: {e}")
    except requests.exceptions.ConnectionError:
        print("✗ Connection error: Unable to reach the server.")
    except requests.exceptions.Timeout:
        print("✗ Timeout error: The request took too long.")
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Ask user for multiple URLs (comma separated)
    urls = input("Please enter one or more image URLs (separated by commas): ").split(",")

    for url in urls:
        url = url.strip()
        if url:  # Ignore empty inputs
            fetch_image(url)

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
