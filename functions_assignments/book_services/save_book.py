import pickle
import os
from .book import Book


class BookRepository:
    def save(self, book: Book) -> None:
        filename = f"/documents/{book.get_title()} - {book.get_author()}"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as file_handle:
            pickle.dump(book, file_handle)

