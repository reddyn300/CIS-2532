import sqlite3
import pandas as pd

connection = sqlite3.connect('books.db')
cursor = connection.cursor()

pd.options.display.max_columns = 10

print("1. View authors table:")
df_authors = pd.read_sql('SELECT * FROM authors', connection, index_col='id')
print(df_authors, "\n")

print("2. View titles table:")
df_titles = pd.read_sql('SELECT * FROM titles', connection)
print(df_titles, "\n")

print("3. View first five rows of author_ISBN table:")
df_author_isbn = pd.read_sql('SELECT * FROM author_ISBN', connection)
print(df_author_isbn.head(), "\n")

print("4. Select first and last names from authors:")
df_names = pd.read_sql('SELECT first, last FROM authors', connection)
print(df_names, "\n")

print("5. Books with copyright year > 2016:")
query = """
SELECT title, edition, copyright
FROM titles
WHERE copyright > '2016'
"""
df_recent_books = pd.read_sql(query, connection)
print(df_recent_books, "\n")

print("6. Authors whose last name starts with 'D':")
query = """
SELECT id, first, last
FROM authors
WHERE last LIKE 'D%'
"""
df_authors_d = pd.read_sql(query, connection, index_col='id')
print(df_authors_d, "\n")

print("7. Authors whose first name matches '_b%':")
query = """
SELECT id, first, last
FROM authors
WHERE first LIKE '_b%'
"""
df_authors_pattern = pd.read_sql(query, connection, index_col='id')
print(df_authors_pattern, "\n")

print("8. Titles ordered ascending by title:")
df_ordered_titles = pd.read_sql('SELECT title FROM titles ORDER BY title ASC', connection)
print(df_ordered_titles, "\n")

print("9. Authors ordered by last name, then first name:")
query = """
SELECT id, first, last
FROM authors
ORDER BY last, first
"""
df_ordered_authors = pd.read_sql(query, connection, index_col='id')
print(df_ordered_authors, "\n")

print("10. Authors ordered by last DESC, first ASC:")
query = """
SELECT id, first, last
FROM authors
ORDER BY last DESC, first ASC
"""
df_ordered_authors_desc = pd.read_sql(query, connection, index_col='id')
print(df_ordered_authors_desc, "\n")

print("11. Titles ending with 'How to Program', ordered by title:")
query = """
SELECT isbn, title, edition, copyright
FROM titles
WHERE title LIKE '%How to Program'
ORDER BY title
"""
df_htp_titles = pd.read_sql(query, connection)
print(df_htp_titles, "\n")

print("12. INNER JOIN authors and author_ISBN, list first, last, isbn:")
query = """
SELECT first, last, isbn
FROM authors
INNER JOIN author_ISBN ON authors.id = author_ISBN.id
ORDER BY last, first
"""
df_join = pd.read_sql(query, connection)
print(df_join.head(), "\n")

print("13. INSERT new author 'Sue Red':")
cursor.execute("""
INSERT INTO authors (first, last)
VALUES ('Sue', 'Red')
""")
connection.commit()

df_authors_after_insert = pd.read_sql('SELECT id, first, last FROM authors', connection, index_col='id')
print(df_authors_after_insert, "\n")

print("14. UPDATE Sue Red's last name to 'Black':")
cursor.execute("""
UPDATE authors SET last='Black'
WHERE last='Red' AND first='Sue'
""")
connection.commit()

print(f"Rows updated: {cursor.rowcount}")

df_authors_after_update = pd.read_sql('SELECT id, first, last FROM authors', connection, index_col='id')
print(df_authors_after_update, "\n")

print("15. DELETE author Sue Black by id:")

df_sue = pd.read_sql("SELECT id FROM authors WHERE first='Sue' AND last='Black'", connection)
if not df_sue.empty:
    sue_id = df_sue.iloc[0]['id']
    cursor.execute('DELETE FROM authors WHERE id = ?', (sue_id,))
    connection.commit()
    print(f"Rows deleted: {cursor.rowcount}")
else:
    print("Sue Black not found.")

df_authors_after_delete = pd.read_sql('SELECT id, first, last FROM authors', connection, index_col='id')
print(df_authors_after_delete, "\n")

connection.close()
