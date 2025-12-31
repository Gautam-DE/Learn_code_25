from typing import List


class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
        self.current_page = 0

    def get_title(self) -> str:
        return self.title

    def get_author(self) -> str:
        return self.author

    def turn_page(self) -> None:
        self.current_page += 1

    def get_current_page(self) -> str:
        return "current page content"

