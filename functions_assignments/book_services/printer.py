from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print_page(self, page: str) -> None:
        pass


class PlainTextPrinter(Printer):
    def print_page(self, page: str) -> None:
        print(page)


class HtmlPrinter(Printer):
    def print_page(self, page: str) -> None:
        print(f'<div style="single-page">{page}</div>')

