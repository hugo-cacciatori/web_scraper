An attemps at a python web scraper for Doctolib.fr, using selenium and beautifulsoup.
# Context
This script aims at scraping the data off of doctolib.fr in order to build a .csv file containing the name, postal address and phone number of every physiotherapist of the PACA region in France. This data was used to conduct a survey that would evaluate the viability of an in development mobile app involving physiotherapists.
# Why selenium ?
Earlier versions of this project were using the python package "requests" in order to send get requests to the doctolib server. However, this method proved unfruitful, as the server security was triggered after about 20 requests, in spite of using a delay of more than 4 seconds in between each request, which obviously wasn't enough to recover the data from more than 450 doctolib profiles. The selenium was found to solve this problem partially, as it emulates more closely the behaviour of a human user. The results were bumped from 20 profiles scraped to about 50, as it still triggers the server security
# Why beautifulsoup ?
Beautifulsoup is a python library that allows html parsing. Here it's used to extract the ld+json tag from the html source code of each profile page that contains the information we are looking for.
# What's next ?
As it stands, the current state of the script does not allow for throughout scraping of doctolib, it's stopped by the doctolib server at roughly 50 entries out of the 450 total. This might be caused by the way the source code of each profile page is currently accessed. The next step would be to find an alternative way to access the ld+json tag that would bypass the server security.
