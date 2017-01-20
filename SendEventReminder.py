#!/usr/bin/env python
# All THIS DOES IS EXECUTES THE SPIDER CRAWL FROM THE COMMAND LINE

from scrapy import cmdline

cmdline.execute("scrapy crawl event_reminder_spider".split())
