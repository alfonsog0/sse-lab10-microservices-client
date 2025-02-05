from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "http://sse-lab10-app.afhfgshhhqhacvdk.uksouth.azurecontainer.io:8080/books"

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/fetch-books")
def fetch_book():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        books = response.json()
        return render_template("results.html", books=books["books"])
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", 500
    
@app.route("/test-api")
def test_api():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()  # Returns the API's response
    except requests.exceptions.RequestException as e:
        return f"API Error: {e}", 500
'''
@app.route("/filter-books")
def filter_books():
    author = request.args.get("author", "").lower()  # Get genre from query string
    try:
        # Fetch all books from the first service
        response = requests.get(API_URL)
        response.raise_for_status()
        books = response.json()["books"]
        
        # Filter books by genre (assuming genre is in the book data)
        filtered_books = [b for b in books if author in b.get("author", "").lower()]
        
        # Render results.html with filtered books
        return render_template("results.html", books=filtered_books)
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", 500
'''
@app.route("/filter-books")
def filter_books():
    # Get the author search parameter from the query string
    author = request.args.get("author", "")
    try:
        # Pass the author parameter to the API service so it filters server side
        params = {}
        if author:
            params["author"] = author
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        books = response.json()["books"]
        return render_template("results.html", books=books)
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", 500

@app.route("/get-book/<int:book_id>")
def get_book(book_id):
    try:
        # Fetch all books from the first service
        response = requests.get(API_URL)
        response.raise_for_status()
        books = response.json()["books"]
        
        # Find the specific book by ID
        book = next((b for b in books if b["id"] == book_id), None)
        
        if book:
            # Render results.html with just the specific book
            return render_template("results.html", books=[book])
        else:
            return f"No book found with ID {book_id}", 404
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)

