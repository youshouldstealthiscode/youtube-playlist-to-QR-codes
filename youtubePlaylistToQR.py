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
youtube = build("youtube", "v3", developerKey="YOUR API KEY")

# Get the playlist details
playlist_id = "insert playlist ID here"
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
    video_id = snippet['resourceId']['videoId'] # Continue from the previous part
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

    # Define the filename
    filename = f'{folder_path}/{re.sub(r"\\W+", "_", snippet["title"])}_QR.png'

    # Save the QR code image
    img.save(filename)

print("All QR codes have been created successfully!")  # Notify the user that the process has completed successfully

#OLDER VERSION
'''
# Import the os module. This module provides functions for interacting with the operating system.
import os
# Import the re module. This module provides regular expression matching operations.
import re
# Import the qrcode module. This module is used for creating QR codes.
import qrcode
# Import the googleapiclient.discovery module. This module is used for interacting with Google APIs.
import googleapiclient.discovery
# Import the ERROR_CORRECT_H constant from the qrcode.constants module. This constant is used for setting the error correction level of a QR code.
from qrcode.constants import ERROR_CORRECT_H

# Define a function called get_minimum_qr_version. This function takes a string of data and returns the minimum QR code version that can encode the data.
def get_minimum_qr_version(data: str) -> int:
    # Get the length of the data.
    data_length = len(data)

    # Create a dictionary that maps QR code versions to their capacities for error correction level H.
    # These capacities are taken from the ISO/IEC 18004:2006(E) document.
    capacities = {
        1: 17,
        2: 32,
        3: 53,
        4: 78,
        5: 106,
        6: 134,
        7: 154,
        8: 192,
        9: 230,
        10: 271,
        11: 321,
        12: 367,
        13: 425,
        14: 458,
        15: 520,
        16: 586,
        17: 644,
        18: 718,
        19: 792,
        20: 858,
        21: 929,
        22: 1003,
        23: 1091,
        24: 1171,
        25: 1273,
        26: 1367,
        27: 1465,
        28: 1528,
        29: 1628,
        30: 1732,
        31: 1840,
        32: 1952,
        33: 2068,
        34: 2188,
        35: 2303,
        36: 2431,
        37: 2563,
        38: 2699,
        39: 2809,
        40: 2953
    }

    # Iterate over the items in the capacities dictionary.
    for version, capacity in capacities.items():
        # If the length of the data is less than or equal to the capacity of the current version, return the version.
        if data_length <= capacity:
            return version

    # If no suitable version was found, raise a ValueError with a descriptive message.
    raise ValueError(f"Data is too long to be encoded in a QR code: {data_length} characters")

# Use the googleapiclient.discovery module to create a service object for the YouTube Data API.
# This service object is used to interact with the API.
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="YOUR API KEY")

# Define the ID of the YouTube playlist you want to work with.
playlist_id = "insert playlist ID here"

# Use the service object to create a request object for the playlists.list method.
# This method is used to retrieve playlist details.
request = youtube.playlists().list(
    part="snippet",  # Specify that you want to retrieve the "snippet" part of the playlist data. The "snippet" part contains basic details about the playlist.
    id=playlist_id,  # Specify the ID of the playlist.
)

# Use the request object to execute the request and get the response.
response = request.execute()

# Get the first item from the "items" list in the response. This item contains the playlist details.
playlist = response["items"][0]

# Get the "title" field from the "snippet" part of the playlist data. This is the title of the playlist.
playlist_title = playlist["snippet"]["title"]

# Create a directory with the same name as the playlist title. This directory will contain the QR codes.
os.makedirs(playlist_title, exist_ok=True)

# Use the service object to create a request object for the playlistItems.list method.
# This method is used to retrieve the items in a playlist.
request = youtube.playlistItems().list(
    part="snippet",  # Specify that you want to retrieve the "snippet" part of the playlist item data.
    maxResults=50,  # Specify the maximum number of items to retrieve per request.
    playlistId=playlist_id,  # Specify the ID of the playlist.
)

# Use a while loop to retrieve all items in the playlist.
while request is not None:
    # Use the request object to execute the request and get the response.
    response = request.execute()

    # Iterate over the items in the "items" list in the response.
    for item in response["items"]:
        # Get the "snippet" part of the playlist item data.
        snippet = item["snippet"]

        # Get the "resourceId" field from the "snippet" part. This field contains the ID of the video.
        video_id = snippet["resourceId"]["videoId"]

        # Create a filename for the QR code. The filename is the title of the video with non-alphanumeric characters replaced by underscores.
        filename = f'{playlist_title}/{re.sub(r"\W+", "_", snippet["title"])}.png'

        # Create the URL of the video.
        url = f'https://www.youtube.com/watch?v={video_id}'

        # Use the get_minimum_qr_version function to get the minimum QR code version that can encode the URL.
        version = get_minimum_qr_version(url)

        # Create a QR code object with the appropriate version and error correction level.
        qr = qrcode.QRCode(
            version=version,
            error_correction=ERROR_CORRECT_H,
        )

        # Add the URL to the QR code.
        qr.add_data(url)

        # Generate the QR code.
        qr.make()

        # Create an image of the QR code with black squares on a white background.
        img = qr.make_image(fill='black', back_color='white')

        # Save the image to a file with the previously created filename.
        img.save(filename)

    # Get the next page token from the response. This token is used to retrieve the next page of items.
    request = youtube.playlistItems().list_next(request, response)
'''

