# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#This is where the data is formatted into an email and sent out
class EventReminderPipeline(object):
	def process_item(self, item, spider):
		test = 0

#UNIMPLEMENTED FOR EVENT REMINDER, 
#CANNOT SEND ARRAY THROUGH PIPELINE
