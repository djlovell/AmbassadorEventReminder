# AmbassadorEventReminder
Python application designed to scrape Kansas State's Engineering Ambassadors event page with the purpose of reminding ambassadors, via email, to sign up for unfilled recruitment events. Events which are unfilled are then formatted into an email and sent internally. I set this up to run from an icon on my Ubuntu Desktop.
# This project was started as a standard scrapy project,but the majority of the code is contained in the "spiders" directory; see "eventSpider.py". 
# The intent was to use a pipeline to manipulate event data and send an email, but I did not find a way to access my entire event array inside the pipeline appropriately. I instead wrote a short amount of script inside the spider itself to send out an email; not pretty, but effective. 

# DISCLAIMER: 
# As a member of KSU's Engineering Ambassador Organization, this app was intended as...
# 1. A personal tool on my own system to make my job of sending event reminders simpler.
# 2. A functional and useful means to start learning python, HTML, and how to scrape web pages! (may not be the prettiest)

# This app is NOT intended to be...
# 1. A public resource. Private account info and passwords have been deleted. I have uploaded to share my learning and growth as a developer!
# 2. A tutorial. See https://scrapy.org/ for good documentation and examples, or google search!
# 3. A "finished product". My goal was to use this as a useful personal learning project, and a first foray into Python/Scraping. 
#    it was exceeded my expectations for functionality, and only small changes will be made as needed.
#    I have commented in ideas for expansion and improvement, but I must devote my time to my coursework and internship with Garmin!

