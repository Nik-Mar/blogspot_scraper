# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

def clean_text(input_string):
    text_content=[string.replace('\n', '') for string in input_string]
    text_content=[string.replace('\t', '') for string in text_content]
    text_content=''.join(text_content).strip()
    return text_content 

class BlogspotPipeline:
    

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # field_names = adapter.field_names()
        # for field_name in field_names:
        #    if field_name == 'text':
        #       post = adapter.get(field_name)
        #       post=clean_text(post)
        #       adapter["field_name"]=post
        text_string= adapter.get("text")
        text_string=clean_text(text_string)   
        adapter["text"]=text_string
        return item
