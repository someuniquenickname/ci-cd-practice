from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
books = [
    {"id": 1, "title": "Concept of Physics", "author": "H.C Verma"},
    {"id": 2, "title": "Gunahon ka Devta", "author": "Dharamvir Bharti"},
    {"id": 3, "title": "Problems in General Physsics", "author": "I.E Irodov"}
]

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(sorted(books, key=lambda x: x["id"]))

# Get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    return jsonify(book) if book else (jsonify({"error": "Book not found"}), 404)

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.json
    if not new_book or not all(key in new_book for key in ["id", "title", "author"]):
        return jsonify({"error": "Missing required fields"}), 400
    books.append(new_book)
    return jsonify(new_book), 201

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.json
    book.update(data)
    return jsonify(book)

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    initial_len = len(books)
    books = [book for book in books if book["id"] != book_id]
    if len(books) < initial_len:
        return jsonify({"message": "Book deleted"}), 200
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
