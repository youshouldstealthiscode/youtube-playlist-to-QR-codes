# Import necessary libraries
# The googleapiclient library is used to access the YouTube API
from googleapiclient.discovery import build
# The os library is used to interact with the operating system, in this case to create directories and files
import os
# The re library is used for regex operations, here to sanitize the video titles
import re
# The qrcode library is used to generate QR codes
import qrcode
# The ERROR_CORRECT_H constant is the highest level of error correction for QR codes
from qrcode.constants import ERROR_CORRECT_H

# Define a function to sanitize video titles, making them safe to use as file names
def sanitize_title(title):
    """
    Sanitize a video title so it can be used as a filename.
    """
    # Use a regex substitution to replace all characters that aren't alphanumeric, whitespace, or hyphen with nothing
    return re.sub(r'[^\w\s-]', '', title)

# Define the main function of the script
def main():
    # Build the YouTube API client
    # Replace "YOUR_API_KEY" with your actual YouTube API key
    youtube = build("youtube", "v3", developerKey="YOUR_API_KEY")

    # Set the playlist ID (replace "PLAYLIST_ID" with your actual playlist ID)
    playlist_id = 'PLAYLIST_ID'

    # Create a request to the YouTube API to get the playlist's details
    playlist_request = youtube.playlists().list(
        part="snippet",  # Get the snippet part of the playlist data, which includes the title
        id=playlist_id  # Specify the ID of the playlist we're interested in
    )

    # Execute the request to the YouTube API
    playlist_response = playlist_request.execute()

    # Extract the playlist title from the response and sanitize it
    playlist_title = sanitize_title(playlist_response['items'][0]['snippet']['title'])

    # Define the path where we'll save the QR code images
    # os.path.expanduser('~') gets the path to the current user's home directory
    # 'Desktop' is then added to that path, followed by the sanitized playlist title
    folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', playlist_title)

    # Use os.makedirs to create the directory at the specified path, if it doesn't already exist
    os.makedirs(folder_path, exist_ok=True)

    # Create a request to the YouTube API to get the items in the playlist
    request = youtube.playlistItems().list(
        part="snippet",  # Get the snippet part of the playlist item data, which includes the video title and ID
        playlistId=playlist_id,  # Specify the ID of the playlist we're interested in
        maxResults=50  # Retrieve up to 50 videos from the playlist
    )

    # Execute the request to the YouTube API
    response = request.execute()

    # Iterate over each video in the playlist
    for item in response['items']:
        # Extract the video details from the item
        video = item['snippet']

        # Extract the video ID from the video details
        video_id = video['resourceId']['videoId']

        # Sanitize the video title
        video_title = sanitize_title(video['title'])

        # Construct the video URL using the video ID
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Create a new QR code object
        qr = qrcode.QRCode(
            version=None,  # Let the library determine the optimal QR code version automatically
            error_correction=ERROR_CORRECT_H,  # Use the highest level of error correction
            box_size=10,  # Set the size of each box in the QR code to 10 pixels
            border=4,  # Set the size of the border around the QR code to 4 boxes
        )

        # Add the video URL to the QR code data
        qr.add_data(video_url)

        # Finalize the QR code data
        qr.make(fit=True)  # Use the 'fit' parameter to optimize the QR code's size automatically

        # Create an image from the QR code data
        # The fill and back colors are set to black and white, respectively
        img = qr.make_image(fill='black', back_color='white')

        # Define the file name for the QR code image
        # It's the sanitized video title with ".png" appended, and it's located in the folder we created earlier
        filename = os.path.join(folder_path, f"{video_title}.png")

        # Save the QR code image to the file
        img.save(filename)

    # Print a message to the console to indicate that the script has finished
    print("Done creating QR codes for each video in the playlist!")

# Call the main function of the script when the script is run
if __name__ == '__main__':
    main()
