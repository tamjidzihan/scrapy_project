# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if value is not None:
                    adapter[field_name] = value[0].strip()

        ## Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if value is not None:
                adapter[lowercase_key] = value.lower()
            
        ## Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value is not None:
                value = value.replace('£', '')
                adapter[price_key] = float(value)


        availability_string = adapter.get("availability")
        split_availability_string = availability_string.split('(')
        if split_availability_string is not  None:
            if len(split_availability_string)>2:
                adapter['availability'] = 0
            else:
                get_number = split_availability_string[1].split(' ')
                adapter['availability'] = int(get_number[0])
        
        
        return item



import psycopg2

class SaveToPostgresPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        db_settings = settings.get('DATABASES')
        return cls(db_settings)

    def open_spider(self, spider):
        self.connection = psycopg2.connect(**self.db_settings)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def create_table(self):
        # Define the table creation SQL statement
        create_table_query = """
            CREATE TABLE IF NOT EXISTS bookscrape (
                id serial PRIMARY KEY,
                title VARCHAR (255),
                product_type VARCHAR (255),
                price NUMERIC,
                price_excl_tax NUMERIC,
                price_incl_tax NUMERIC,
                availability VARCHAR (255),
                description TEXT,
                category VARCHAR (255)
            );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def process_item(self, item, spider):
        # Create the table if it doesn't exist
        self.create_table()

        # Insert data into the table
        insert_query = """
            INSERT INTO bookscrape (title, product_type, price, price_excl_tax, price_incl_tax, availability, description, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        self.cursor.execute(insert_query, (
            item['title'],
            item['product_type'],
            item['price'],
            item['price_excl_tax'],
            item['price_incl_tax'],
            item['availability'],
            item['description'],
            item['category'],
        ))
        self.connection.commit()
        return item

