# Import the necessary libraries
import os  # Library for interacting with the OS
import re  # Regular expressions library
import qrcode  # Library for creating QR codes
from qrcode.constants import ERROR_CORRECT_H  # Importing a constant for error correction level
from googleapiclient.discovery import build  # Google API client

def get_minimum_qr_version(data: str) -> int:
    """
    This function returns the smallest QR code version that can fit the given data string.
    It is based on the character capacities provided in the ISO/IEC 18004:2006(E) document.
    """
    # Determine the length of the input data
    data_length = len(data)

    # Version-capacity mappings for error correction level H.
    # These are taken from the ISO/IEC 18004:2006(E) document.
    capacities = {
        1: 17, 2: 32, 3: 53, 4: 78, 5: 106, 6: 134, 7: 154, 8: 192, 9: 230,
        10: 271, 11: 321, 12: 367, 13: 425, 14: 458, 15: 520, 16: 586, 17: 644,
        18: 718, 19: 792, 20: 858, 21: 929, 22: 1003, 23: 1091, 24: 1171,
        25: 1273, 26: 1367, 27: 1465, 28: 1528, 29: 1628, 30: 1732, 31: 1840,
        32: 1952, 33: 2068, 34: 2188, 35: 2303, 36: 2431, 37: 2563, 38: 2699,
        39: 2809, 40: 2953
    }

    # Iterate over the capacities, and find the smallest version that can accommodate the data
    for version, capacity in capacities.items():
        if data_length <= capacity:
            return version  # Return the version if the capacity is enough

    # If no suitable version was found, raise an error
    raise ValueError(f"Data is too long to be encoded in a QR code: {data_length} characters")


# Build the Youtube service
youtube = build("youtube", "v3", developerKey="YOUR_API_KEY")

# Get the playlist details
playlist_id = "YOUTUBE_PLAYLIST_ID"
request = youtube.playlists().list(
    part="snippet",
    id=playlist_id
)
response = request.execute()

# Get the playlist title
playlist_title = response['items'][0]['snippet']['title']

# Define the folder path where QR codes will be saved
folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', playlist_title)

# Make the directory if it doesn't exist already
os.makedirs(folder_path, exist_ok=True)

# Get the playlist items
request = youtube.playlistItems().list(
    part="snippet",
    maxResults=50,
    playlistId=playlist_id
)
response = request.execute()

# Iterate over the items and create QR codes
for item in response['items']:
    snippet = item['snippet']
    video_title = snippet['title']
    video_id = snippet# Continue from the previous part
    video_id = snippet['resourceId']['videoId']  # Get the video ID from the snippet

    # Define the video URL
    video_url = f"https://youtu.be/{video_id}"  # Concatenate the base Youtube URL with the video ID to create the full URL

    # Create a QR code object
    qr = qrcode.QRCode(
        version=get_minimum_qr_version(video_url),  # Set the version based on the URL length
        error_correction=ERROR_CORRECT_H,  # Set the error correction level to H
        box_size=10,  # Set the size of the QR code box
        border=4,  # Set the border size
    )

    # Add the video URL to the QR code object
    qr.add_data(video_url)

    # Finalize the QR code object
    qr.make(fit=True)

    # Create an image from the QR code object
    img = qr.make_image(fill='black', back_color='white')

    # Remove any non-alphanumeric characters from the video title and replace them with underscores
    title_for_filename = re.sub(r"\W+", "_", snippet["title"])
    # Append "_QR.png" to the title to indicate that this file is a QR code
    # The filename is then joined with the folder_path to get the full path of the image file
    filename = f'{folder_path}/{title_for_filename}_QR.png'



    # Save the QR code image
    img.save(filename)

print("All QR codes have been created successfully!")  # Notify the user that the process has completed successfully
