"""Library Manager - a simple terminal program to manage a small library.

You can add books, list them, search, borrow, return, delete,
and see statistics. Data is saved in a file called library.json.
"""

import json
import os

DATA_FILE = "library.json"


# ---------- Saving and loading ----------

def load_books():
    """Read the books from the file. Return an empty dictionary if no file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_books(books):
    """Write all the books to the file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)


# ---------- Helper functions ----------

def get_next_id(books):
    """Return the next free book ID as text (1, 2, 3, ...)."""
    if not books:
        return "1"
    return str(max(int(book_id) for book_id in books) + 1)


def print_book(book_id, book):
    """Print one book on a single line."""
    if book["borrowed_by"]:
        status = "Borrowed by " + book["borrowed_by"]
    else:
        status = "Available"
    print(f"[{book_id}] {book['title']} - {book['author']} "
          f"({book['year']}) - {status}")


# ---------- Menu actions ----------

def add_book(books):
    print("\n--- Add a Book ---")
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year = input("Year published: ").strip()

    if not year.isdigit():
        print("The year must be a number. Book not added.")
        return

    book_id = get_next_id(books)
    books[book_id] = {
        "title": title,
        "author": author,
        "year": int(year),
        "borrowed_by": None,
    }
    save_books(books)
    print(f"Book added with ID {book_id}.")


def show_books(books):
    print("\n--- All Books ---")
    if not books:
        print("The library is empty.")
        return

    for book_id in sorted(books, key=int):
        print_book(book_id, books[book_id])


def search_books(books):
    print("\n--- Search ---")
    keyword = input("Enter a title or author to search for: ").strip().lower()

    found = False
    for book_id in sorted(books, key=int):
        book = books[book_id]
        if keyword in book["title"].lower() or keyword in book["author"].lower():
            print_book(book_id, book)
            found = True

    if not found:
        print("No books found.")


def borrow_book(books):
    print("\n--- Borrow a Book ---")
    book_id = input("Enter the book ID: ").strip()

    if book_id not in books:
        print("There is no book with that ID.")
        return

    if books[book_id]["borrowed_by"]:
        print("Sorry, this book is already borrowed.")
        return

    name = input("Borrower name: ").strip()
    books[book_id]["borrowed_by"] = name
    save_books(books)
    print(f"'{books[book_id]['title']}' is now borrowed by {name}.")


def return_book(books):
    print("\n--- Return a Book ---")
    book_id = input("Enter the book ID: ").strip()

    if book_id not in books:
        print("There is no book with that ID.")
        return

    if not books[book_id]["borrowed_by"]:
        print("This book was not borrowed.")
        return

    books[book_id]["borrowed_by"] = None
    save_books(books)
    print(f"'{books[book_id]['title']}' has been returned.")


def delete_book(books):
    print("\n--- Delete a Book ---")
    book_id = input("Enter the book ID: ").strip()

    if book_id not in books:
        print("There is no book with that ID.")
        return

    answer = input(f"Delete '{books[book_id]['title']}'? (y/n): ").strip().lower()
    if answer == "y":
        del books[book_id]
        save_books(books)
        print("Book deleted.")
    else:
        print("Cancelled.")


def show_statistics(books):
    print("\n--- Library Statistics ---")
    total = len(books)
    borrowed = sum(1 for book in books.values() if book["borrowed_by"])

    print(f"Total books: {total}")
    print(f"Available: {total - borrowed}")
    print(f"Borrowed: {borrowed}")

    if books:
        oldest = min(books.values(), key=lambda book: book["year"])
        print(f"Oldest book: {oldest['title']} ({oldest['year']})")


# ---------- Main program ----------

def show_menu():
    print("\n===== Library Manager =====")
    print("1. Add a book")
    print("2. Show all books")
    print("3. Search for a book")
    print("4. Borrow a book")
    print("5. Return a book")
    print("6. Delete a book")
    print("7. Show statistics")
    print("0. Exit")


def main():
    books = load_books()

    actions = {
        "1": add_book,
        "2": show_books,
        "3": search_books,
        "4": borrow_book,
        "5": return_book,
        "6": delete_book,
        "7": show_statistics,
    }

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice](books)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
