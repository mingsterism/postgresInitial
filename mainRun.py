from actions import DatabaseConn

def main():
	cities = DatabaseConn('config.ini', 'DBSettings')
	cities.executeCommand("CREATE TABLE countries (country_code char(2) PRIMARY KEY, country_name text UNIQUE);")
	cities.executeCommand("""INSERT INTO countries (country_code, country_name) VALUES ('us', 'United States'), ('mx', 'Mexico'), ('au', 'Australia'), 
		('gb', 'United Kingdom'), ('de', 'Germany'), ('my', 'Malaysia');""")
	print(cities.readData("SELECT * FROM countries;"))
	cities.executeCommand("""CREATE TABLE cities (name text NOT NULL, postal_code varchar(9) CHECK (postal_code <> ''), country_code char(2) REFERENCES countries,
							PRIMARY KEY (country_code, postal_code));""")
	cities.executeCommand("INSERT INTO cities VALUES ('Portland', '87200', 'us');")
	cities.executeCommand("UPDATE cities SET postal_code = '99900' WHERE name = 'Portland';")
	print(cities.readData("SELECT cities.*, country_name FROM cities INNER JOIN countries ON cities.country_code = countries.country_code;"))
	cities.executeCommand("""CREATE TABLE venues (venue_id SERIAL PRIMARY KEY, name varchar(255), street_address text, type char(7) CHECK (type in ('public', 'private') ) 
							DEFAULT 'public', postal_code varchar(9), country_code char(2), FOREIGN KEY (country_code, postal_code) REFERENCES cities (country_code, postal_code) MATCH FULL);""")
	print(cities.readData("SELECT v.venue_id, v.name, c.name FROM venues v INNER JOIN cities c ON v.postal_code=c.postal_code AND v.country_code=c.country_code;"))
	print("closing connection....")
	cities.conn.close()



if __name__ == '__main__':
	main()