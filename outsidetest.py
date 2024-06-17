# Importing Sqlite3 Module
import sqlite3
import datetime
import random

def create_new_category(cur, name):
	now = datetime.datetime.now()
	id = random_with_N_digits(4)
	sql = """
    INSERT INTO articles_category(id, name)
	VALUES(?, ?)
    """
	cur.execute(sql, (id, name))
	cur.commit()

def create_new_issue(cur, theme, num, vol):
	now = datetime.datetime.now()
	id = random_with_N_digits(4)
	sql = """
    INSERT INTO articles_issue(id, name, num, vol)
	VALUES(?, ?, ?, ?)
    """
	cur.execute(sql, (id, theme, num, vol))
	cur.commit()
def add_article(conn, title, slug, author_id, body, issue_id, category_id):
	now = datetime.datetime.now()
	id = random_with_N_digits(8)
	post = (id, title, f"{now}", f"{now}", slug, body)
	auth = (id, id, author_id)
	iss = (id, id, issue_id)
	cat = (id, id, category_id)
	sql = """
    INSERT INTO articles_post(id, title, last_modified, created_on, slug, body)
	VALUES(?, ?, ?, ?, ?, ?)
    """
	author = """
    INSERT INTO articles_post_authors(id, post_id, author_id)
	VALUES(?, ?, ?)
    """
	issue = """
    INSERT INTO articles_post_issues(id, post_id, issue_id)
	VALUES(?, ?, ?)
    """

	category =  """
    INSERT INTO articles_post_categories(id, post_id, category_id)
	VALUES(?, ?, ?)
    """
	cur = conn.cursor()
	cur.execute(sql, post)
	cur.execute(author, auth)
	cur.execute(issue, iss)
	cur.execute(category, cat)
	conn.commit()
	return cur.lastrowid
test_values = ("test_title", "test_slug", 1, "lorem ipsum", 4, 3)
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    random.seed(datetime.datetime.now().timestamp())
    i = random.randint(range_start, range_end)
    form = str(i).zfill(n)
    return form
try:
	
	sqliteConnection = sqlite3.connect('readme/db.sqlite3')

	print("Connected to SQLite")

	sql_query = """SELECT name FROM sqlite_master 
	WHERE type='table';"""
	cursor = sqliteConnection.cursor()
	cursor.execute(sql_query)
	print("List of tables\n")
	print(cursor.fetchall())
	cursor.execute("""SELECT * FROM articles_category""")
	print(cursor.description)
	title, slug, author_id, body, issue_id, category_id = test_values
	print(id)#add_article(sqliteConnection, art)
	print(cursor.fetchall())
	#create_new_category(sqliteConnection, "Letter from the Editor")
	#add_article(sqliteConnection, title, slug, author_id, body, issue_id, category_id)
	


except sqlite3.Error as error:
	print("Failed to execute the above query", error)
	
finally:

	# Inside Finally Block, If connection is
	# open, we need to close it
	if sqliteConnection:
		
		# using close() method, we will close 
		# the connection
		sqliteConnection.close()
		
		# After closing connection object, we 
		# will print "the sqlite connection is 
		# closed"
		print("the sqlite connection is closed")
