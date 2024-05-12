import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import models

def main():
    DBMS = 'postgresql'
    user = 'postgres'
    password = 'izvara32'
    host = 'localhost:5432'
    db_name = 'salebook_db'
    DSN = f'{DBMS}://{user}:{password}@{host}/{db_name}'
    engine = sq.create_engine(DSN)

    models.create_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    models.create_table(engine)
    models.fill_in_the_data(session)

    pk = input("Введите имя или индентификатор издателя: ")

    subq = (session.query(models.Sale, models.Shop, models.Book).join(models.Stock.sale)
            .join(models.Book, models.Stock.id_book == models.Book.id)
            .join(models.Publisher, models.Publisher.id == models.Book.id_publisher)
            .join(models.Shop, models.Shop.id == models.Stock.id_shop).filter(models.Publisher.name==pk))

    for s in subq.all():
        line = '%-45s | %-20s | %-7.2f | %-10s' % (s.Book.title, s.Shop.name, s.Sale.price, str(s.Sale.date_sale))
        print(line)

    session.close()

if __name__ == '__main__':
    main()



