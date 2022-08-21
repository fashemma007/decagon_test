import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from sql_queries import table_names, create_table_queries
import os
from dotenv import load_dotenv

load_dotenv()
HOST=os.getenv('HOST')
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
PORT=os.getenv('PORT')
DATABASE_NAME=os.getenv('DATABASE_NAME')


cnx = mysql.connector.connect(user='root',passwd=PASSWORD)
cursor = cnx.cursor()

countries_url = 'https://raw.githubusercontent.com/annexare/Countries/master/data/countries.json'
continents_url = 'https://raw.githubusercontent.com/annexare/Countries/master/data/continents.json'
languages_url = 'https://raw.githubusercontent.com/annexare/Countries/master/data/languages.json'
countries_iso_url = 'https://raw.githubusercontent.com/annexare/Countries/master/data/countries.2to3.json'

def extract_data():
	"""
	Extracting all data required
	"""
	countries_df = pd.read_json(countries_url)
	continents_df = pd.read_json(continents_url,typ='series')
	languages_df = pd.read_json(languages_url)
	countries_iso_df = pd.read_json(countries_iso_url,typ='series')
	
	return countries_df,continents_df,languages_df,countries_iso_df

def transforms():
	#=======================Working on countries=======================
	countries= countries_df.T
	countries= countries.reset_index()
	countries.rename(columns = {'index':'country_id', 
								'native':'native_name',
								'name':'country_name',
								'currency':'currency_id', 
								'languages':'language_id',
								'phone':'country_code',
								'continent':'continent_id'},inplace = True)
	countries['currency_id'] = [','.join(i) if isinstance(i, list) else i for i in countries['currency_id']]
	countries['language_id'] = [','.join(i) if isinstance(i, list) else i for i in countries['language_id']]
	countries['country_code'] = [i[0] for i in countries['country_code']]
	countries.drop(['continents'], axis=1, inplace = True)

	#==========Working on is02-iso3=======================
	c_iso_df = countries_iso_df.to_frame()
	c_iso_df.reset_index(inplace = True)
	c_iso_df.rename(columns = {'index':'country_id',0:'country_id_3' }, inplace = True)
	
	#=======================Merging countries and iso-codes=======================
	countries_iso_merge=pd.merge(countries,c_iso_df, on ='country_id')
	countries_iso_merge = countries_iso_merge[['country_name','capital','native_name','country_id','country_id_3', 'country_code','currency_id','language_id','continent_id']]
	
	#==========Working on continents=======================
	continent_df = continents_df.to_frame()
	continent_df.reset_index(inplace = True)
	continent_df.rename(columns = {'index':'continent_id',0:'name' }, inplace = True)
	continent_df=continent_df[['continent_id','name']]
	
	#==========Working on Languages=======================
	language_df = languages_df.T
	language_df.reset_index(inplace = True)
	language_df.rename(columns = {'index':'language_id', 'native':'native_name','name':'language'}, inplace = True)
	language_df.drop('rtl',axis=1, inplace = True)
	language_df=language_df[['language_id','language','native_name']]
	
	#==========Extracting a currencies table=======================
	currency_countries = countries_iso_merge[['country_id','currency_id']].copy()
	currency_countries = currency_countries.groupby('currency_id')['country_id'].apply(list)
	currency_countries = currency_countries.to_frame().reset_index()
	currency_countries['country_id'] = [','.join(x) if isinstance(x, list) else x for x in currency_countries['country_id']]
	currency_countries = currency_countries.reset_index().rename(columns={'index':'id'})
	currency_countries = currency_countries.set_index(['id','country_id'])\
	.apply(lambda x: x.str.split(',').explode()).reset_index()
	currency_countries = currency_countries[currency_countries['currency_id']!='']
	currency_countries =currency_countries.drop(['id'], axis=1).reset_index().rename(columns={'index':'id'})
	currency_countries = currency_countries[['id','currency_id','country_id']]
	
	return countries_iso_merge,continent_df,language_df,c_iso_df,currency_countries

#=======================Dropping Database=======================
def drop_db(cursor):	
	cursor.execute("DROP DATABASE IF EXISTS {}".format(DATABASE_NAME))
	print("{} Database dropped ".format((DATABASE_NAME)))


def create_database(cursor):
	try:
			cursor.execute(
					"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DATABASE_NAME))
			print("Database {} created successfully.".format(DATABASE_NAME))
			cursor.execute("USE {}".format(DATABASE_NAME))
	except mysql.connector.Error as err:
			print("Failed creating database: {}".format(err))
			exit(1)

		
def connect_to_db(cursor):
	cnx.database = DATABASE_NAME
	cursor.execute("USE {}".format(DATABASE_NAME))

#=======================Creating tables=======================
def create_tables(cursor):
	for i,table_name in enumerate(create_table_queries):
		try:
			print(f"Creating table {table_names[i]}: ", end='')
			cursor.execute(table_name)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				print(f"{table_names[i]} already Exists.")
			else:
				print(err.msg)
		else:
			print("Successful")

def load(cursor):
	print("===========Loading data into Countries table============")
	countries_tuple = [tuple(r) for r in country_df.to_numpy()]
	try:
		cursor.execute("USE {}".format(DATABASE_NAME))
		
		countries_insert_query = """INSERT INTO countries (name, capital, native_name, country_id, country_id_3, country_code, currency_code, language_id, continent_id) 
								VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """

		cursor.executemany(countries_insert_query, countries_tuple)
		cnx.commit()
		print(cursor.rowcount, "Record inserted successfully into countries table")

	except mysql.connector.Error as error:
		print("Failed to insert countries record into MySQL countries table {}".format(error))
	
	print("===========Loading data into Continents Table=============")
	continent_tuple = [tuple(r) for r in continent_df.to_numpy()]
	try:
			
		continents_insert_query = """INSERT INTO continents (continent_id,name) 
								VALUES (%s, %s) """
		cursor.executemany(continents_insert_query, continent_tuple)
		cnx.commit()
		print(cursor.rowcount, "Record inserted successfully into continents table")

	except mysql.connector.Error as error:
		print("Failed to insert continents record into MySQL continents table {}".format(error))

	print("===========Loading data into languages table============")
	language_tuple = [tuple(r) for r in language_df.to_numpy()]

	try:
		languages_insert_query = """INSERT INTO languages (language_id, name, native_name) 
		VALUES (%s, %s, %s) """
		cursor.executemany(languages_insert_query, language_tuple)
		cnx.commit()
		print(cursor.rowcount, "Record inserted successfully into languages table")

	except mysql.connector.Error as error:
		print("Failed to insert languages record into MySQL languages table {}".format(error))   
	
	print("===========Loading data into Currency Table============")
	currency_tuple = [tuple(r) for r in currency_countries.to_numpy()]
	try:
		currency_insert_query = """INSERT INTO currency (id,currency_code, country_id) 
		VALUES (%s, %s, %s ) """
		cursor.executemany(currency_insert_query, currency_tuple)
		cnx.commit()
		print(cursor.rowcount, "Record inserted successfully into currency table")

	except mysql.connector.Error as error:
		print("Failed to insert currency record into MySQL currency table {}".format(error))	 




if __name__ == "__main__":
	countries_df,continents_df,languages_df,countries_iso_df = extract_data()
	country_df,continent_df,language_df,country_iso_df,currency_countries= transforms()
	drop_db(cursor)
	create_database(cursor)
	connect_to_db(cursor)
	create_tables(cursor)
	load(cursor)
