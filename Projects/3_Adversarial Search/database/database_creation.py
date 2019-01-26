import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="admin"
)

class Database:

	def __init__(self):
		self.mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="admin",
			database="isolation"
		)

	def build_database(self):
		mycursor = self.mydb.cursor()
		try:
			mycursor.execute("CREATE DATABASE Isolation")
		except Exception as e:
			print(e)

	def create_table(self):
		mycursor = self.mydb.cursor()
		try:
			mycursor.execute("USE Isolation")
			mycursor.execute("CREATE TABLE userdata (\
													  board varchar(255),\
													  p1 varchar(255),\
													  p2 varchar(255),\
													  turn varchar(255),\
													  value float,\
													  primary key (board, p1, p2, turn)\
													);")		 
		except Exception as e:
			print(e)		

	def insert(self,board,p1,p2,turn,value):
		mycursor = self.mydb.cursor()
		sql = "INSERT INTO userdata (board, p1, p2, turn, value) VALUES (%s, %s, %s, %s, %s)"
		val = (board, p1, p2, turn, value)
		try:
			mycursor.execute(sql, val)
		except Exception as e:
			print(e)		
			
database = Database()
# database.build_database()	
# database.create_table()	
database.insert("123123","123","123","0",12.3)