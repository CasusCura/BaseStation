def deleteUser(self, conn, username):
	cursor = conn.cursor()

	# Build and execute the update
	query = ('DELETE FROM radcheck WHERE username=%s')
	cursor.execute(query, (username))

	# Ensure data has been committed
	conn.commit()

	# Close the connection
	cursor.close()

	# User deletion was successful
	return True
