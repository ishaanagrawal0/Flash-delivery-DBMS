import mysql.connector

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="flash"
)
db_cursor = db_connection.cursor()

# Define the trigger query
trigger_query = """
CREATE TRIGGER update_order_history_trigger
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Insert a record into order_history table with details of the newly placed order
    INSERT INTO order_history (total_cost, deliver_address, order_id, customer_id)
    VALUES (NEW.final_price, NEW.billing_address, NEW.order_id, NEW.customer_id);
END;
"""
# Execute the trigger query
db_cursor.execute(trigger_query)
# Commit the changes
db_connection.commit()


# Define the trigger query
trigger_query = """
CREATE TRIGGER clear_cart_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Delete cart items for the customer who placed the order
    DELETE FROM cart WHERE customer_id = NEW.customer_id;
END;
"""
# Execute the trigger query
db_cursor.execute(trigger_query)
# Commit the changes
db_connection.commit()

# Close the cursor and database connection
db_cursor.close()
db_connection.close()
