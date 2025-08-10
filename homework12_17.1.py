import sqlite3
import pandas as pd

connection = sqlite3.connect('books.db')
cursor = connection.cursor()

print("1. Authors' last names in descending order:")
df1 = pd.read_sql('SELECT last FROM authors ORDER BY last DESC', connection)
print(df1, "\n")

print("2. Book titles in ascending order:")
df2 = pd.read_sql('SELECT title FROM titles ORDER BY title ASC', connection)
print(df2, "\n")

author_first = 'Paul'
author_last = 'Deitel'

query = f"""
SELECT titles.title, titles.copyright, titles.isbn
FROM titles
INNER JOIN author_ISBN ON titles.isbn = author_ISBN.isbn
INNER JOIN authors ON author_ISBN.id = authors.id
WHERE authors.first = '{author_first}' AND authors.last = '{author_last}'
ORDER BY titles.title ASC
"""

print(f"3. Books by {author_first} {author_last}:")
df3 = pd.read_sql(query, connection)
print(df3, "\n")

print("4. Inserting new author 'John Doe':")
cursor.execute("""
INSERT INTO authors (first, last)
VALUES (?, ?)
""", ('John', 'Doe'))
connection.commit()

df4 = pd.read_sql('SELECT id, first, last FROM authors WHERE first = "John" AND last = "Doe"', connection)
print(df4, "\n")

print("5. Inserting new title for author 'John Doe':")

author_id = df4.iloc[0]['id']

new_isbn = '9999999999'  
new_title = "Adventures in SQL"
new_edition = 1
new_copyright = '2025'

cursor.execute("""
INSERT INTO titles (isbn, title, edition, copyright)
VALUES (?, ?, ?, ?)
""", (new_isbn, new_title, new_edition, new_copyright))

cursor.execute("""
INSERT INTO author_ISBN (id, isbn)
VALUES (?, ?)
""", (author_id, new_isbn))

connection.commit()

query_confirm = f"""
SELECT authors.first, authors.last, titles.title, titles.isbn
FROM authors
INNER JOIN author_ISBN ON authors.id = author_ISBN.id
INNER JOIN titles ON author_ISBN.isbn = titles.isbn
WHERE authors.id = {author_id}
"""

df5 = pd.read_sql(query_confirm, connection)
print(df5, "\n")

connection.close()
