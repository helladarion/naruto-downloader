import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import sys
from os.path import expanduser

"""
We check the site gogoanimes.co for Naruto Shippuden episodes
"""
if len(sys.argv[1:]) == 1:
    episode = str(sys.argv[1:][0])
else:
    episode = input("What Naruto Shippuden episode do you want to download? ")

home = expanduser("~")
# Directory you want to save the videos
videoDir = home + "/Videos/Naruto/"

# Base address to get the episodes
address = 'https://gogoanimes.co/naruto-shippuden-episode-' + episode
# Grabbing html code
site = requests.get(address)

if site.ok: # if site is online continue
    # Parse the site for readability
    soup = BeautifulSoup(site.content, 'html.parser')
    # find the line with the address for download
    link = soup.find_all(href=re.compile('https://vid'))
    # Extract only the link
    vidsite = requests.get(link[0]['href'])
    # Parse this new address
    soup2 = BeautifulSoup(vidsite.content, 'html.parser')
    #find the download line and extract the download link in a single line
    downloadLink = soup2.find_all(href=re.compile('https://st1'))[0]['href']
    # Getting the episode file itself and trying to stream it
    file = requests.get(downloadLink, stream=True)
    # Checking total size of the episode
    total_size = int(file.headers.get('content-length', 0))
    """
    Creating the episode file in mp4 format and partially saving it
    """
    with open(videoDir + 'NarutoShippuden-' + episode + '.mp4', 'wb') as f:
        print("Downloading Episode " + episode)
        with tqdm(total=total_size / (32*1024.0), unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for data in file.iter_content(32*1024):
                f.write(data)
                pbar.update(len(data))
else:
    print("Site not found")

