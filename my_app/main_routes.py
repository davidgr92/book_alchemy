from flask import Blueprint, render_template, request, redirect, url_for, flash
import book_alchemy.data_manager.dm_sqlite as dm_sqlite
from my_app import db

main = Blueprint('main', __name__)
dm = dm_sqlite.SqliteDataManager(db.session)


@main.route('/', methods=["GET", "POST"])
def home():
    """
    Home page rendering function, if used with POST request sorts the books
    :return: Returns html rendered file
    """
    if request.method == "POST":
        orderby = request.form.get("order_column")
        direction = bool(request.form.get("direction"))

        sorted_books = dm.get_sorted_data_from_db(join=True,
                                                  order_column=orderby,
                                                  direction=direction)

        return render_template('home.html', books=sorted_books)

    return render_template('home.html',
                           books=dm.get_data_from_db(db_model=dm_sqlite.Book,
                                                     join=True))


@main.route('/add_author', methods=["GET", "POST"])
def add_author():
    """
    Add author page rendering function, if used with POST request,
    Adds a new author to database
    :return: Returns html rendered file
    """
    if request.method == "POST":
        name = request.form.get("name")
        date_of_birth = request.form.get("birthdate")
        date_of_death = request.form.get("date_of_death")
        message = dm.add_new_author(name=name, date_of_birth=date_of_birth,
                                    date_of_death=date_of_death)
        flash(message)
    return render_template('add_author.html')


@main.route('/add_book', methods=["GET", "POST"])
def add_book():
    """
    Add book page rendering function, if used with POST request,
    Adds a new book to database
    :return: Returns html rendered file
    """
    if request.method == "POST":
        title = request.form.get("title")
        isbn = request.form.get("isbn")
        publication_year = request.form.get("publication_year")
        author_id = request.form.get("author")

        message = dm.add_new_book(title=title, isbn=isbn,
                                  publication_year=publication_year,
                                  author_id=author_id)
        flash(message)
    return render_template('add_book.html',
                           authors=dm.get_data_from_db())


@main.route('/search_results', methods=["GET", "POST"])
def search_data():
    """
    If used with POST request, loads search results by provided params
    otherwise redirects to home function
    :return: Returns html rendered file
    """
    if request.method == "POST":
        search_column = request.form.get("search_column")
        search_query = request.form.get("search_query")

        filtered_books = dm.get_filtered_data_from_db(search_column,
                                                      search_query)
        return render_template('home.html', books=filtered_books)
    return redirect(url_for('main.home'))


@main.route('/book/<int:book_id>')
def show_single_book(book_id):
    """
    Renders and returns single book data template
    :param book_id: Book id in database
    :return: Returns html rendered file
    """
    book, author = dm.get_filtered_data_from_db("book_id", book_id, limit=1)
    return render_template("single_book.html", book=book, author=author)


@main.route('/book/<int:book_id>/delete', methods=["GET", "POST"])
def delete_book(book_id):
    """
    Deletes book entry from the database
    :param book_id: Book id in database
    :return: redirects to home function
    """
    if request.method == "POST":
        dm.delete_entry_from_db(book_id)
        flash("Successfully deleted the book.")
        return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))


@main.route('/authors')
def show_authors():
    """
    Gets authors data from database and renders html file with the data
    :return: Returns html rendered file
    """
    authors = dm.get_data_from_db()
    return render_template("authors.html", authors=authors)


@main.route('/author/<int:author_id>')
def show_single_author(author_id):
    """
    Gets author data and the books by that author,
    renders the data in template and returns html file
    :param author_id: Author id in database
    :return: Returns html rendered file
    """
    books_author = dm.get_filtered_data_from_db("author_id", author_id)
    books = [book for book, author in books_author]
    author = books_author[0][1]
    return render_template("single_author.html", books=books, author=author)


@main.route('/author/<int:author_id>/delete', methods=["GET", "POST"])
def delete_author(author_id):
    """
    Deletes author entry from the database, if he has books in database
    first deletes all the books and finally deletes the author.
    :param author_id: Author id in database
    :return: redirects to home function
    """
    if request.method == "POST":
        dm.delete_entry_from_db(author_id, db_model=dm_sqlite.Author)
        flash("Successfully deleted the author.")
        return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))
