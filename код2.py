import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import models


def creating_a_connection(dbms, user, password, host, db_name):
    dsn = f'{dbms}://{user}:{password}@{host}/{db_name}'
    engine = sq.create_engine(dsn)

    models.create_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    models.create_table(engine)
    models.fill_in_the_data(session)
    return session


def get_shops(db_session, key):

    subq = db_session.query(models.Book.title, models.Shop.name, models.Sale.price, models.Sale.date_sale).\
            select_from(models.Sale).\
            join(models.Stock, models.Sale.id_stock == models.Stock.id).\
            join(models.Book, models.Stock.id_book == models.Book.id).\
            join(models.Publisher, models.Publisher.id == models.Book.id_publisher).\
            join(models.Shop, models.Shop.id == models.Stock.id_shop)
    if key.isdigit():
        subq = subq.filter(models.Publisher.id==key).all()
    else:
        subq = subq.filter(models.Publisher.name==key).all()
    for title, shop, price, date_sale in subq:
        line = '%-45s | %-20s | %-7.2f | %-10s' % (title, shop, price, str(date_sale))
        print(line)

    db_session.close()

if __name__ == '__main__':
    DBMS = 'postgresql'
    USER = 'postgres'
    PASSWORD = 'izvara32'
    HOST = 'localhost:5432'
    DB_NAME = 'salebook_db'
    session = creating_a_connection(DBMS, USER, PASSWORD, HOST, DB_NAME)
    key_user = input("Введите имя или индентификатор издателя: ")
    get_shops(session, key_user)
