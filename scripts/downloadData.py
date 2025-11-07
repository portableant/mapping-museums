import requests
import os

# --- Configuration ---
URL = "https://museweb.dcs.bbk.ac.uk/static/pdf/MappingMuseumsData2021_09_30.csv"
DATA_DIR = "data"
FILE_NAME = URL.split("/")[-1] # Extracts the filename from the URL
FULL_PATH = os.path.join(DATA_DIR, FILE_NAME)

def download_csv(url, path):
    """
    Downloads a file from a URL and saves it to a specified path.
    """
    # 1. Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    print(f"Attempting to download file from: {url}")
    print(f"Saving to: {path}")

    try:
        # 2. Send an HTTP GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # 3. Write the content to the file in binary mode ('wb')
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print("\n✅ Download successful!")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ An error occurred during the download: {e}")

if __name__ == "__main__":
    # Ensure you have the 'requests' library installed: pip install requests
    download_csv(URL, FULL_PATH)