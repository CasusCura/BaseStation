def listUsers(conn):
	cursor = conn.cursor()

	# Build and execute the query
	query = ("SELECT username FROM radcheck")
	cursor.execute(query)

	# Build the results set
	users = [username[0] for username in cursor]

	# Close the connection
	cursor.close()

	# Returns an array containing all of the users
	return users
