import scrapy
from AmbassadorEventReminder.items import EventItem
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

'''
This spider crawls Kansas State University's Engineering Ambassador
website in order to email members about unfilled event sign-ups
'''
class EventReminderSpider(CrawlSpider):
    name = 'event_reminder_spider'
    start_urls = ['https://www.engg.ksu.edu/enggamb/eaonline/events.php']

    #default parse method will perform login
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'user': '[USERNAME]', 'password': '[PASSWORD]'},
            callback=self.scrape_event_info
        )
    #scrapes event information and sends a properly formatted email
    def scrape_event_info(self, response):
        tables = Selector(response).xpath('//div[@id="primaryContent"]/table[contains(@width, "780px")]')
        events = []
        tableIterator = 0
        #variables hold info for events as they are added to the array
        current_title = ""
        current_date = ""
        current_location = ""
        current_startTime = ""
        current_endTime = ""
        current_description = ""
        current_memberText = ""
        for table in tables:
            tableIterator += 1
            if (tableIterator%2)!=0 :
                current_title = table.xpath('tr[1]/td/text()').extract()
                current_date = table.xpath('tr[2]/td/text()').extract()
            else :
                '''
                full events are of the td_eventtime_mem class in a td tag.
                empty events (desired) are contained in td_eventtime_mem_red classes
		        '''
                trTags = table.xpath('tr') #extracts all 3*n tr tags, n = # time slots
                trIterator = 0
                for tr in trTags:
                    trIterator += 1
                    if trIterator == 2 :
                        current_location = tr.xpath('td[1]/text()').extract()
                        current_startTime = tr.xpath('td[2]/text()').extract()
                        current_endTime = tr.xpath('td[3]/text()').extract()
                        current_description = tr.xpath('td[4]/text()').extract()
                    elif trIterator == 3 :
                        current_memberText = tr.xpath('td/text()').extract()
                        event = EventItem()
                        event["title"] = current_title[0].encode('utf-8')
                        event["date"] = current_date[0].encode('utf-8')
                        event["location"] = current_location[0].encode('utf-8')
                        event["startTime"] = current_startTime[0].encode('utf-8')
                        event["endTime"] = current_endTime[0].encode('utf-8')
                        event["description"] = current_description[0].encode('utf-8')
                        memberString = current_memberText[0].encode('utf-8')
                        numberNeededOnward = memberString.partition("Number Needed: ")[2]
                        tempTuple = numberNeededOnward.partition("Number Signed Up: ")
                        value_numberNeeded = int(tempTuple[0].partition("\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\n")[0])
                        value_numberSoFar = int(tempTuple[2])
                        event["numberDesired"] = value_numberNeeded
                        event["numberSignedUp"] = value_numberSoFar
                        event["numberEmptySpots"] = value_numberNeeded-value_numberSoFar
                        if value_numberNeeded-value_numberSoFar > 0 :
                            events.append(event)
                        trIterator = 0 #reset iterator, looking at sets of 3

        #Formatting information for an email
        greetingText = "Greetings fellow Engineering Ambassadors!\n\n\tIn the spirit "+\
		"of keeping on top of our upcoming events and saving time during meetings, "+\
         "\nplease check your calendars and sign up for the following "+\
		"unfilled event times before the next meeting!\n\n"

        eventEmailTexts = ""
        previousEventTitle = ""
        eventIndex = 0
        for event in events :
            if eventIndex < 1000 : #Change this line if you want to only email out a specific number of events
                if event['title'] != previousEventTitle:
                    eventEmailTexts += ("\n\t"+ event['title'] +
                    " on " + event['date'] + "\n").upper()
                eventEmailTexts += "\n\t\tTIME: " + event['startTime'] + " to " + event['endTime'] +\
                             " @ " + event["location"] + "\n\t\tNEEDED: " + str(event['numberEmptySpots']) +\
                             " more ambassadors! (" + str(event['numberSignedUp']) + "/" +\
                              str(event['numberDesired']) + " have signed up)\n"
                previousEventTitle = event['title']
            eventIndex += 1
        salutation = "\n\nHave a great week! Until next time," +\
                    "\n\nDaniel J. Lovell\nJunior|Computer Engineering" +\
                    "\nKansas State University"

        fromaddr = "[FROM ADDRESS]"
        toaddr = "[TO ADDRESS]"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "ENG AMB EVENT REMINDER"
        body = greetingText + eventEmailTexts + salutation
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "[EMAIL PASSWORD]")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text) #uncomment to send email
        server.quit()

        return

        '''
        FUTURE IMPROVEMENTS/IDEAS
        1. Learn proper Python syntax and formatting...this is a professional tool
        2. Find way to either save event dictionary array externally or return 
           from this spider to enable use in external classes/files
        3. (See above) Delegate data/email formatting to an external script,
           couldn't figure out how to do this without pipelining, which didn't work
        4. Set up and test on Windows 10
        5. Run from a standalone flash drive? (could make copies for other ambassadors)
        6. Turn this into a mobile Android App or WebApp
        7. Figure out how to use School (Microsoft 365) email instead of personal,
           to make List-serve access easier for myself and other members 

