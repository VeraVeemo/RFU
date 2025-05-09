import os
import random
import sys
import requests
import json

cats = []

if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")):
    print("Images directory/folder not found, creating...")
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images"))
    print("\nCreated!\n")

for root, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")):
    for file in files:
        if file.endswith((".png", ".jpg", ".jpeg", ".webm", ".webp")):
            path = os.path.join(root, file)
            cats.append(path)
            print(f"Collected file {path}!")

print("")
try:
    output = random.choice(cats)
    name = os.path.basename(output)
except:
    print("Please put files into the \"Images\" folder before running this")
    input("\nPress enter to continue and close program.")
    sys.exit()

with open("../../config.json", "r") as file:
    data = json.load(file)

ChannelID = data["ChannelID"]
AuthToken = data["DiscordAuthToken"]

if ChannelID == 1234567890:
    print("Please configure your Channel ID before running this executable!\nGo to the \"config.json\" file and change \"ChannelID\" to match the ID you want to send to.")
    input("\nPress enter to continue and close program.")
    sys.exit()
elif AuthToken == "":
    print("Please configure your Discord Authentication Token before running this executable!\nGo to the \"config.json\" file and change \"DiscordAuthToken\" to your Discord Token.")
    input("\nPress enter to continue and close program.")
    sys.exit()

file = open(output, "rb")

headers = { "Authorization": AuthToken }
files = { "file": (file.name, file, "application/octet-stream" ) }

print(f"Uploading file \"{name}\"...\n")
response = requests.post(
    f"https://discord.com/api/v10/channels/{ChannelID}/messages", headers=headers, files=files)

file.close()

if response.status_code == 200:
    print("File uploaded successfully!")
elif response.status_code == 400:
    print("Bad Request: The request was invalid or cannot be processed.")
    print("Error details:", response.json())
elif response.status_code == 401:
    print("Unauthorized: The bot token is invalid or missing.")
elif response.status_code == 403:
    print("Forbidden: You don't have permission to post in this channel.")
elif response.status_code == 404:
    print("Not Found: The channel doesn't exist or is invalid.")
elif response.status_code == 429:
    print("Too Many Requests: You're being rate-limited.")
    retry_after = response.json().get('retry_after', 0)
    print(f"Try again after {retry_after} seconds.")
elif response.status_code == 500:
    print("Internal Server Error: Something went wrong on Discord's end.")
elif response.status_code == 502:
    print("Bad Gateway: Discord's servers are down.")
elif response.status_code == 503:
    print("Service Unavailable: Discord's API is unavailable.")
elif response.status_code == 504:
    print("Gateway Timeout: Discord's API timed out.")
else:
    print(f"Unexpected error: {response.status_code}")
    print("Error details:", response.json())