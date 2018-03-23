def updateUser(conn, username, password):
	cursor = conn.cursor()

	# Build and execute the update
	query = ('UPDATE radcheck SET passsword=%s WHERE username=%s')
	cursor.execute(query, (passsword, username))

	# Ensure data has been committed
	conn.commit()

	# Close the connection
	cursor.close()

	#User update was successful
	return True
