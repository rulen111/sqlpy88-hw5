# SQLPY-88 Homework #5. ORM. Student Akhmarov Ruslan
# Main python script file

# Imports
import yaml
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Publisher, Stock, Book, Shop, Sale, create_tables, drop_tables, pop_from_json


# Define search function
def find_sales_pub(publisher, session):
    """
    Gets sales entries from DB corresponding to the provided publisher.
    Prints the result and returns nothing
    :param publisher: publisher id (int) or name (str) to search for
    :param session: sqlalchemy Session object
    :return: None
    """
    if publisher.isnumeric():
        q = session.query(
            Publisher.name,
            Book.title,
            Shop.name,
            Sale.price,
            Sale.count,
            Sale.date_sale
        ).join(
            Book, Book.id_publisher == Publisher.id
        ).join(
            Stock, Stock.id_book == Book.id
        ).join(
            Sale, Sale.id_stock == Stock.id
        ).join(
            Shop, Shop.id == Stock.id_shop
        ).filter(
            Publisher.id == int(publisher)
        )
        for s in q.all():
            print(f"{s.title:<60}| {s.name:<19}| {s.price*s.count:<7}| {s.date_sale}")
    else:
        q = session.query(
            Publisher.name,
            Book.title,
            Shop.name,
            Sale.price,
            Sale.count,
            Sale.date_sale
        ).join(
            Book, Book.id_publisher == Publisher.id
        ).join(
            Stock, Stock.id_book == Book.id
        ).join(
            Sale, Sale.id_stock == Stock.id
        ).join(
            Shop, Shop.id == Stock.id_shop
        ).filter(
            Publisher.name == publisher
        )
        for s in q.all():
            print(f"{s.title:<60}| {s.name:<19}| {s.price*s.count:<7}| {s.date_sale}")


# Script payload
if __name__ == "__main__":
    # Read config file
    with open("config.yaml") as c:
        config = yaml.full_load(c)

    # Make DSN string
    DSN = (f'{config["DB"]["PROTOCOL"]}://{config["DB"]["USER"]}:'
           f'{config["DB"]["PASSWORD"]}@{config["DB"]["SERVER"]}:'
           f'{config["DB"]["PORT"]}/{config["DB"]["NAME"]}')

    # Initialize Engine object
    engine = sq.create_engine(DSN)

    # Drop existing tables and create them again
    drop_tables(engine)
    create_tables(engine)

    # Initialize Session object
    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert test data from json file
    pop_from_json("tests_data.json", session)

    # Repeated search
    flag = True
    while flag:
        publisher = input("Введите имя или идентификатор издателя: ")
        print("-"*50)
        find_sales_pub(publisher, session)
        print("-"*50)
        flag = True if input("Повторить поиск? [y/n]") == "y" else False
        print("")
