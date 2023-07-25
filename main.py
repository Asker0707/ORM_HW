import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from models import create_tables, Publisher, Book, Stock, Sale, Shop 

DSN = 'postgresql://postgres:superuser@localhost:5432/infobook'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


author = input('Введите имя автора (Например: Pearson) или id: ')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)
if author.isdigit():
    query = query.filter(Publisher.id == author).all()
else:
    query = query.filter(Publisher.name == author).all()

for title, name, price, date_sale in query:
    print(f"{title} | {name} | {price} | {date_sale}")



session.close()