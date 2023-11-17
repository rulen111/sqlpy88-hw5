# SQLPY-88 Homework #5. ORM. Student Akhmarov Ruslan
# Sqlalchemy model description file

# Imports
import sqlalchemy as sq
import json
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

# Initialize Base object
Base = declarative_base()


# Define Publisher relation
class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)


# Define Stock relation
class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer(), sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer(), sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.SmallInteger)


# Define Book relation
class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")
    stocks = relationship(Stock, backref="book")


# Define Shop relation
class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    books = relationship(Stock, backref="shop")


# Define Sale relation
class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(5, 2), nullable=False)
    date_sale = sq.Column(sq.DateTime, default=datetime.now())
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.SmallInteger)

    stock = relationship(Stock, backref="sales")


# Define functions for tables setup
def create_tables(engine):
    """
    Creates all tables using defined structure
    :param engine: sqlalchemy Engine object
    :return: None
    """
    Base.metadata.create_all(engine)


def drop_tables(engine):
    """
    Deletes all tables from DB
    :param engine: sqlalchemy Engine object
    :return: None
    """
    Base.metadata.drop_all(engine)


def pop_from_json(fp, session):
    """
    Populates created DB tables with entries from .json file
    :param fp: filepath to a .json file
    :param session: sqlalchemy Session object
    :return: None
    """
    with open(fp, "r") as f:
        data = json.load(f)

    for row in data:
        table = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale
        }[row.get("model")]

        session.add(table(id=row.get("pk"), **row.get("fields")))
    session.commit()
