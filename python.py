from abc import ABC, abstractmethod
from datetime import datetime

class book(ABC):
    def __init__(self,  isbn: str, title: str, author: str, year: int, price: float = 0):
        self.isbn = isbn
        self.price = price
        self.author = author
        self.title = title
        self.year = year
    
    @abstractmethod
    def purchase(self, quantity: int, email: str, address: str):
        pass

    @abstractmethod
    def book_details(self):
        pass

    def is_outdated(self, expire_date):
        current_year = datetime.now().year
        return (current_year - self.year) > expire_date

class paperBook(book):
    bookType = "Paper Book"
    def __init__(self, isbn: str, title: str, price: float, stock: int, year: int, author: str = None):
        super().__init__(isbn, title, author, year, price)
        self.stock = stock

    def purchase(self, email, address, quantity: int = 1):
        if not address or not email:
            raise ValueError("Quantum book store: Please enter your Address and email.")
        
        if quantity > self.stock:
            raise ValueError(f"Quantum book store: Sorry, there is only {self.stock} books remaning.")
        
        print(f"Quantum book store: Book {self.isbn} has been purchased successfully.")

        # sheping service
        ShippingService.Shipping(self.isbn, address)

        # Remove sold books from inventory
        self.stock -= quantity

        return self.price * quantity
    
    def book_details(self):
        print(f"*** Book {self.isbn} Details ***")
        print(f"Title: {self.title}")
        print(f"Price: {self.price}")
        print(f"Stock: {self.stock}")
        print(f"Year: {self.year}")
        print(f"Author: {self.author}")
        print(f"bookType: {self.bookType}")
        return

class eBook(book):
    bookType = "EBook"
    # def __init__(self, isbn: str, title: str, price: float, fileType: int, year: int, author: str = None):
    def __init__(self, isbn: str, title: str, price: float, year: int, author: str = None, fileType: int = "Unknown"):
        super().__init__(isbn, title, author, year, price)
        self.fileType = fileType

    def purchase(self, email, address, quantity: int = 1):
        if quantity != 1:
            raise ValueError("Quantum book store: EBook can be purchased one time only.")

        if not address or not email:
            raise ValueError("Quantum book store: Please enter your Email and Address.")
        
        print(f"Quantum book store: Book {self.isbn} has been purchased successfully.")

        # sheping service 
        MailService.Shipping(self.isbn, email)

        return self.price
    
    def book_details(self):
        print(f"*** Book {self.isbn} Details ***")
        print(f"Title: {self.title}")
        print(f"Price: {self.price}")
        print(f"Year: {self.year}")
        print(f"Author: {self.author}")
        print(f"bookType: {self.bookType}")
        print(f"fileType: {self.fileType}")

class showcaseBook(book):
    bookType = "Showcase Book"
    def __init__(self, isbn: str, title: str, year: int, author: str):
        super().__init__(isbn, author, title, year)

    def purchase(self, quantity: int = 0, email: str = None, address: str = None):
        raise ValueError("Quantum book store: Sorry, Showcase Books is not for sale.")
    
    def book_details(self):
        print(f"*** Book {self.isbn} Details ***")
        print(f"Title: {self.title}")
        print(f"Year: {self.year}")
        print(f"Author: {self.author}")
        print(f"bookType: {self.bookType}")
        return

class ShippingService:
    @staticmethod
    def Shipping(isbn, address):
        print(f"ShippingService: Book: {isbn} will be shepped to adress in two days.")

class MailService:
    @staticmethod
    def Shipping(isbn, mail):
        print(f"ShippingService: Book: {isbn} hase been send to mail: {mail}.")

class BookStore:
    def __init__(self):
        self.inventory: dict[str, book] = {}

    def add(self, book: book):
        self.inventory[book.isbn] = book
        print(f"Quantum book store: '{book.title}' book Added to inventory")

    def buy(self, isbn, email, adress, quntity = 1):
        book = self.inventory.get(isbn, None)
        if(book):
            paid_amount = book.purchase(email, adress, quntity)
            print(f"Paid amount: {paid_amount}$")
        else:
            raise ValueError(f"Quantum book store: Sorry, we didn`t have this book in our store.")

    def remove_outdated_books(self, expDate: int):
        print("Removing outdated Books...")
        flag = False
        for isbn in list(self.inventory.keys()):
            book = self.inventory[isbn]
            if (book.is_outdated(expDate)):
                flag = True
                print(f"Removing book {book.isbn}.")
                self.inventory.pop(isbn)
        if(flag == False):
            print(f"No expired books to remove.")


class SystemTestClass:
    @staticmethod
    def run_tests():
        print("Quantum book store: Starting comprehensive tests...")

        # initialize some books as example
        harry_botter_book = paperBook("1", "harry botter", 100, 5, 2023, "George Orwell")
        The_Stranger = eBook("2", "The Stranger", 100, 2021, "Ernest Hemingway", "pdf")
        The_Metamorphosis = showcaseBook("3", "The Metamorphosis", 2015, "John Steinbeck")

        # print all book details with built on function 
        harry_botter_book.book_details()
        The_Stranger.book_details()
        The_Metamorphosis.book_details()

        # initialize book store
        Quantum_book_store = BookStore()

        # try to add some books
        Quantum_book_store.add(harry_botter_book)
        Quantum_book_store.add(The_Stranger)
        Quantum_book_store.add(The_Metamorphosis)

        print(harry_botter_book.stock) # 5
        # buy book example
        Quantum_book_store.buy("1", 'test@gmail.com', '6 october', 3) # Quantum book store: Book 1 has been purchased successfully.
        print(harry_botter_book.stock) # 2

        # an error raised: Quantum book store: EBook can be purchased one time only.
        # Quantum_book_store.buy("2", 'Abdelrahman@gmail.com', 'zaid', 3) 

        Quantum_book_store.buy("2", 'Abdelrahman@gmail.com', 'zaid', 1) 

        # Remove and return outdated books that passed specific number of years
        Quantum_book_store.remove_outdated_books(5)

SystemTestClass.run_tests()

