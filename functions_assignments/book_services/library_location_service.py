from .book import Book


class LibraryLocationService:
    def get_location(self, book: Book) -> str:
        return "Shelf A3, Room 2"

