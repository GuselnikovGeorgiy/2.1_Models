from datetime import date
from database import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Genre(BaseModel):
    """Название жанра"""

    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        unique=True,
    )
    name_genre: Mapped[str] = mapped_column(unique=True)

    book: Mapped["Book"] = relationship("Book", back_populates="genre")


class Author(BaseModel):
    """Автор"""

    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    name_author: Mapped[str] = mapped_column(unique=True)

    book: Mapped["Book"] = relationship("Book", back_populates="genre")


class Book(BaseModel):
    """Название книги, цена, количество на складе, id жанра и автора"""

    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.genre_id"))
    price: Mapped[float]
    amount: Mapped[int]

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")
    buy_books: Mapped["BuyBook"] = relationship("BuyBook", back_populates="book")


class City(BaseModel):
    """Город клиента и время доставки в днях"""

    __tablename__ = "cities"

    city_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    name_city: Mapped[str] = mapped_column(unique=True)
    days_delivery: Mapped[int]

    client: Mapped["Client"] = relationship("Client", back_populates="city")


class Client(BaseModel):
    """Имя клиента, почта, id города"""

    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    name_client: Mapped[str] = mapped_column(unique=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.city_id"))
    email: Mapped[str] = mapped_column(unique=True)

    city: Mapped["City"] = relationship("City", back_populates="clients")
    buys: Mapped["Buy"] = relationship("Buy", back_populates="client")


class Buy(BaseModel):
    """Пожелания клиента и id клиента"""

    __tablename__ = "buys"

    buy_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    buy_description: Mapped[str]
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id"))

    client: Mapped["Client"] = relationship("Client", back_populates="buys")
    buy_books: Mapped["BuyBook"] = relationship("BuyBook", back_populates="buy")
    buy_steps: Mapped["BuyStep"] = relationship("BuyStep", back_populates="buy")


class BuyBook(BaseModel):
    """Таблица с количеством заказанных книг, id книги и таблица пожеланий клиента"""

    __tablename__ = "buy_books"

    buy_book_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    buy_id: Mapped[int] = mapped_column(ForeignKey("buys.buy_id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id"))
    amount: Mapped[int]

    buy: Mapped["Buy"] = relationship("Buy", back_populates="buy_books")
    book: Mapped["Book"] = relationship("Book", back_populates="buy_books")


class Step(BaseModel):
    """Этапы обработки заказа клиента"""

    __tablename__ = "steps"

    step_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    name_step: Mapped[str] = mapped_column(unique=True)

    buy_steps: Mapped["BuyStep"] = relationship("BuyStep", back_populates="step")


class BuyStep(BaseModel):
    """Даты начала и конца этапов обработки заказа с данными клиента и этапа"""

    __tablename__ = "buy_steps"

    buy_step_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True
    )
    buy_id: Mapped[int] = mapped_column(ForeignKey("buys.buy_id"))
    step_id: Mapped[int] = mapped_column(ForeignKey("steps.step_id"))
    date_step_beg: Mapped[date]
    date_step_end: Mapped[date]

    buy: Mapped["Buy"] = relationship("Buy", back_populates="buy_steps")
    step: Mapped["Step"] = relationship("Step", back_populates="buy_steps")
