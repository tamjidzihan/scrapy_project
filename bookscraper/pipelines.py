# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # price_keys = ['price', 'price_excl_tax', 'price_incl_tax']
        # for price_key in price_keys:
        #     value = adapter.get(price_key)
        #     value = value.replace('£', '')
        #     adapter[price_key] = float(value)


        # field_names = adapter.field_names()
        # for field_name in field_names:
        #     value = adapter.get(field_name)
        #     print('********')
        #     adapter[field_name] = value[0].strip()

        # lowercase_keys = ['catagory','product_type']
        # for lowercase_key in lowercase_keys:
        #     value = adapter.get(lowercase_key)
        #     print(f'####################{value}####################################################')
        #     adapter[lowercase_key] = value.lower()

        # price_keys = ['price','price_excl_tax','price_incl_tax']
        # for price in price_keys:
        #     value = adapter.get(price)
        #     new_value = value.replace('£','')
        #     adapter[new_value] = float(new_value)

        
        return item

