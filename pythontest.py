import random
books = [
            {'bookId': '123', 'title': 'Dummy Book 1', 'author': 'Author 1'},
            {'bookId': '456', 'title': 'Dummy Book 2', 'author': 'Author 2'},
            {'bookId': '321', 'title': 'Dummy Book 3', 'author': 'Author 3'},
            {'bookId': '654', 'title': 'Dummy Book 4', 'author': 'Author 4'},
            {'bookId': '132', 'title': 'Dummy Book 5', 'author': 'Author 5'},
            {'bookId': '465', 'title': 'Dummy Book 6', 'author': 'Author 6'}
        ]

        # Randomly choose 2 books
books2 = random.sample(books, 2)

print(books2)