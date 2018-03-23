def insertUser(conn, username, password):
	cursor = conn.cursor()

	# Build and execute the query
	query = ('INSERT INTO radcheck (username, attribute, op, value) VALUES(%s, "Cleartext-Password", ":=", %s);')
	cursor.execute(query, (username, password))

	# Ensure data has been committed
	conn.commit()

	# Close the connection
	cursor.close()

	# User insertion was successful
	return True
