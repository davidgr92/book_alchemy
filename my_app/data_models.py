from my_app import db


class Author(db.Model):
    """
    Author model class, which sets the columns for "authors" table
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"Author: {self.name}, id: {self.id}"


class Book(db.Model):
    """
    Book model class, which sets the columns for "books" table
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    cover_url = db.Column(db.String, nullable=True)

    # Foreign Key
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"),
                          nullable=False)

    def __repr__(self):
        return f"<Book(id = {self.id}, name = {self.title}, " \
               f"publication_year = {self.publication_year})>"

    def __str__(self):
        return f"Book: {self.title}, id: {self.id}"
