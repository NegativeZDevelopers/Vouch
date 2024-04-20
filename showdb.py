import sqlite3
import os
os.system("cls")
def control_db(database_file, query, params=None):
    """
    Execute a database query and commit changes.

    Args:
        database_file (str): Path to the SQLite database file.
        query (str): SQL query to execute.
        params (tuple, optional): Parameters for the query (if any). Default is None.

    Returns:
        None
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Execute the query with optional parameters
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    # Commit the changes
    conn.commit()

    # Close the database connection
    conn.close()
def view_database(database_path):
    os.system("cls")
    # Fetch the list of available tables
    tables = []
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        # Print available tables
        print("Available tables:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        # Let the user choose a table
        table_index = int(input("Enter the number corresponding to the table you want to modify: ")) - 1
        table_name = tables[table_index]

        # Execute a SELECT query to fetch all rows from the selected table
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()

        # Print the current contents of the table
        print("\nCurrent contents of the table:")
        column_names = [description[0] for description in cursor.description]
        print(", ".join(column_names))
        for row in rows:
            print(", ".join(map(str, row)))

        # Ask the user for action: remove all, remove by line, add, or edit
        action = input("\nEnter 'remove all', 'remove line', 'add', 'edit', or 'exit': ").lower()

        if action == 'remove all':
            # Execute a DELETE query to remove all rows from the selected table
            control_db(database_path, f'DELETE FROM {table_name}')
            print("All rows removed from the table.")

        elif action == 'remove line':
            # Ask the user for the line number to remove
            line_number = int(input("Enter the line number to remove: ")) - 1

            if 0 <= line_number < len(rows):
                # Execute a DELETE query to remove the specified row
                row_to_remove = rows[line_number]
                control_db(database_path, f"DELETE FROM {table_name} WHERE rowid=?", (row_to_remove[0],))
                print(f"Row {line_number + 1} removed from the table.")
            else:
                print("Invalid line number. No changes made.")

        elif action == 'add':
            # Ask the user for new data to add
            new_data = input("Enter comma-separated values for the new row: ")
            new_data_values = tuple(new_data.split(','))

            # Execute an INSERT query to add a new row
            control_db(database_path, f'INSERT INTO {table_name} VALUES ({",".join("?" * len(new_data_values))})', new_data_values)
            print("New row added to the table.")

        elif action == 'edit':
            # Ask the user for the line number to edit
            line_number = int(input("Enter the line number to edit: ")) - 1

            if 0 <= line_number < len(rows):
                # Ask the user for new data
                new_data = input("Enter comma-separated values for the edited row: ")
                new_data_values = tuple(new_data.split(','))

                # Execute an UPDATE query to edit the specified row
                row_to_edit = rows[line_number]
                update_query = f"UPDATE {table_name} SET {','.join(f'{column}=?' for column in column_names)} WHERE rowid=?"
                control_db(database_path, update_query, (*new_data_values, row_to_edit[0]))

                print(f"Row {line_number + 1} edited in the table.")
            else:
                print("Invalid line number. No changes made.")

        elif action == 'exit':
            exit()

        else:
            print("Invalid action. No changes made.")

    except (ValueError, IndexError):
        print("Invalid input. Exiting.")

    finally:
        # Close the database connection
        conn.close()
print("Database Want to look :")
database = input(">> ") 
if not database:
    database ='vouch_db_1.1.sql'
while True:
    view_database(database)

