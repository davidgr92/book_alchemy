from flask import flash
from datetime import datetime
from book_alchemy.my_app.data_models import Author, Book
from book_alchemy.apis.isbndb_api import get_book_cover_by_isbn


class SqliteDataManager:
    """
    Sqlite data interface manager, interacts with the sqlite database.
    """
    def __init__(self, db_session):
        self.db_session = db_session

    @staticmethod
    def convert_str_to_date(date_string):
        """
        Converts date string input to a datetime object
        :param date_string: date string from form
        :return: Datetime object
        """
        date_format = "%Y-%m-%d"
        return datetime.strptime(date_string, date_format)

    @staticmethod
    def validate_num_by_len(num, req_len):
        """
        Validate input data is in the correct length
        :param num: Number to validate
        :param req_len: Required length for validation
        :return: Returns true if num is in the correct length
        otherwise returns false
        """
        if len(str(num)) == req_len:
            return True
        return False

    @staticmethod
    def get_sort_search_column(col_str):
        """
        Get sort/search object
        :param col_str: Column string
        :return: returns a database model property for sort/search
        """
        if col_str == "title":
            return Book.title
        elif col_str == "name":
            return Author.name
        elif col_str == "author_id":
            return Author.id
        elif col_str == "book_id":
            return Book.id
        else:
            raise ValueError("Invalid col_str value")

    def get_sorting_object(self, sort_column, direction):
        """
        Gets sorting object by column and ascending variables
        :param sort_column: column by which to sort
        :param direction: if True direction is ascending, otherwise descending
        :return: returns an order_by object with the database model
        and direction of sorting
        """
        orderby_column = self.get_sort_search_column(sort_column)
        return orderby_column.asc() if direction \
            else orderby_column.desc()

    def validate_date(self, date_string):
        """
        Checks if a valid date value exists, if it does, converts it to
        date object, otherwise returns none.
        :param date_string: Date string input from form
        :return: Returns date object if date_string is a valid date value
        and not empty, otherwise returns none.
        """
        if date_string:
            try:
                return self.convert_str_to_date(date_string)
            except ValueError as ve:
                flash(f"Error while parsing date, date was not added: {ve}")

    def get_data_from_db(self, db_model=Author, join=False):
        """
        Fetches data from the database based on provided db_model,
        and optional parameters. By default, fetches from 'authors' table.
        :param db_model: database model
        :param join: if set to True returns a joined table
        :return: returns an iterable of entries from the database
        based on the provided table
        """
        query = self.db_session.query

        if join:
            data = query(Book, Author).join(Author).all()
        else:
            data = query(db_model).all()

        return data

    def get_sorted_data_from_db(self, db_model=Author, join=False,
                                order_column="name", direction=True):
        """
        Fetches and sorts data from the database based on provided db_model,
        and optional parameters. By default, fetches from 'authors' table,
        and sorts based on author 'name'.
        :param db_model: database model
        :param join: if set to True returns data from a joined table.
        :param order_column: column by which to order, by default set to "name"
        :param direction: if True direction is ascending, otherwise descending
        :return: returns an iterable of entries from the database
        based on the provided table and sorted by order_column and direction.
        """
        query = self.db_session.query

        if join:
            orderby_obj = self.get_sorting_object(order_column, direction)
            data = query(Book, Author).join(Author)\
                .order_by(orderby_obj).all()
        else:
            orderby_obj = self.get_sorting_object(order_column, direction)
            data = query(db_model).order_by(orderby_obj).all()

        return data

    def get_filtered_data_from_db(self, filter_column, search_q, limit=None):
        """
        Gets filtered data from database based on search column
        and search query.
        :param filter_column: Based on what column to search the data
        :param search_q: What to search in provided search column
        :param limit: if defined, limits the reponse
        :return:
        """
        query = self.db_session.query
        filter_column = self.get_sort_search_column(filter_column)
        f_search_q = f"%{search_q}%"
        if limit == 1:
            data = query(Book, Author).join(Author).\
                filter(filter_column.like(f_search_q)).one()
        elif limit:
            data = query(Book, Author).join(Author).\
                filter(filter_column.like(f_search_q)).limit(limit)
        else:
            data = query(Book, Author).join(Author).\
                filter(filter_column.like(f_search_q)).all()

        return data

    def add_data_to_db(self, new_data_entry):
        """
        Adds new data object to the corresponding table
        :param new_data_entry: database object (Author/Book object)
        """
        self.db_session.add(new_data_entry)
        self.db_session.commit()

    def add_new_author(self, name, date_of_birth, date_of_death):
        """
        Checks provided parameters, and adds a new entry to authors database.
        :param name: Author name
        :param date_of_birth: Author date of birth, can be empty.
        :param date_of_death: Author date of death, can be empty.
        :return: Returns a success message with the added author details
        """
        dob_date_obj = self.validate_date(date_of_birth)
        dod_date_obj = self.validate_date(date_of_death)

        new_author = Author(name=name, birth_date=dob_date_obj,
                            date_of_death=dod_date_obj)
        self.add_data_to_db(new_author)

        return f"Successfully added {new_author}"

    def add_new_book(self, title, isbn, publication_year, author_id):
        """
        Checks provided parameters, and adds a new entry to books database.
        :param title: Book title
        :param isbn: Book unique isbn code
        :param publication_year: Original publication year of the book
        :param author_id: Author id
        :return: Returns a success message with the added book details
        """
        if not self.validate_num_by_len(isbn, 13):
            raise ValueError("Wrong ISBN value")
        if not self.validate_num_by_len(publication_year, 4):
            raise ValueError("Wrong publication year")

        cover_url = get_book_cover_by_isbn(isbn)
        new_book = Book(title=title, isbn=isbn, publication_year=publication_year,
                        author_id=author_id, cover_url=cover_url)

        self.add_data_to_db(new_book)

        return f"Successfully added {new_book}"

    def delete_entry_from_db(self, item_id, db_model=Book):
        if db_model == Author:
            books_by_author = self.get_filtered_data_from_db("author_id", item_id)
            for book, author in books_by_author:
                self.delete_entry_from_db(book.id)
            self.db_session.query(db_model).filter(db_model.id == item_id).delete()
        else:
            self.db_session.query(db_model).filter(db_model.id == item_id).delete()

        self.db_session.commit()
