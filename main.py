import mysql.connector
import matplotlib.pyplot as plt

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="flash"
)
db_cursor = db_connection.cursor()
customer_id = 0


def is_valid_email(email):
    return "@" in email

def admin_login_menu():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    query = f"SELECT * FROM admin WHERE Email_id = '{email}' AND Password = '{password}'"
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    if result:
        print("Logged in successfully!")
        admin_id = result[0]
        admin_menu(admin_id)
    else:
        print("Login failed. Please check your credentials.")

def customer_login_menu():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    query = f"SELECT * FROM customer WHERE Email_id = '{email}' AND Password = '{password}'"
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    customer_id = result[0]
    if result:
        print("Logged in successfully!")
        customer_menu(customer_id)
    else:
        print("Login failed. Please check your credentials.")
        return

def customer_signup():
    email = input("Enter your email: ")
    if not is_valid_email(email):
        print("Invalid email address. Please include an '@' in the email address.")
        return
    username = input("Enter your username: ")
    age = int(input("Enter your age: "))
    address = input("Enter your address: ")
    password = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
    else:
        query = f"INSERT INTO customer (customer_name, Age, Address, Email_id, Password) VALUES ('{username}', {age}, '{address}', '{email}', '{password}')"
        db_cursor.execute(query)
        db_connection.commit()
        customer_id = db_cursor.lastrowid
        print("Customer Signup successful!")
        print("Do you wish to login now?")
        print("1. Yes")
        print("2. No")
        login_choice = int(input("Enter your choice: "))
        if login_choice == 1:
            customer_login_menu()
        if login_choice == 2:
            print("Thank you for visiting FLASH Online Shopping Portal!")
            return
        else:
            print("Invalid option.")
            return
        
def add_products_to_cart(customer_id):
    product_id = int(input("Enter the product ID you want to add to cart: "))
    quantity = int(input("Enter the quantity: "))
    add_to_cart(product_id, quantity, customer_id)
    return

def add_to_cart_helper(customer_id):
    print("Do you want to add products to cart?")
    print("1. Yes")
    print("2. No")
    add_to_cart_choice = int(input("Enter your choice: "))
    if add_to_cart_choice == 1:
        while True:
            add_products_to_cart(customer_id)
            print("Do you want to add more products to cart?")
            print("1. Yes")
            print("2. No")
            add_more_choice = int(input("Enter your choice: "))
            if add_more_choice != 1:
                return
    return

def view_all_products():
    try:
        transaction_cursor = db_connection.cursor()

        # Start transaction
        transaction_cursor.execute("START TRANSACTION")

        query = "SELECT * FROM product"
        transaction_cursor.execute(query)
        products = transaction_cursor.fetchall()

        # Commit the transaction
        db_connection.commit()

        if products:
            print("All Products:")
            for product in products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Price: {product[3]}")
        else:
            print("No products available at the moment.")

    except mysql.connector.Error as err:
        # Rollback the transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        db_connection.rollback()

    finally:
        transaction_cursor.close()

def view_products_by_category():
    try:
        transaction_cursor = db_connection.cursor()

        # Start transaction
        transaction_cursor.execute("START TRANSACTION")

        query = "SELECT * FROM category"
        transaction_cursor.execute(query)
        categories = transaction_cursor.fetchall()

        for category in categories:
            print(f"Category ID: {category[0]}, Name: {category[1]}")

        category_id = int(input("Enter the category ID you want to view: "))
        query = f"SELECT * FROM product WHERE category_id = {category_id}"
        transaction_cursor.execute(query)
        products = transaction_cursor.fetchall()

        # Commit the transaction
        db_connection.commit()

        if products:
            print("Products in Selected Category:")
            for product in products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Price: {product[3]}")
        else:
            print("No products available in this category.")

    except mysql.connector.Error as err:
        # Rollback the transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        db_connection.rollback()

    finally:
        transaction_cursor.close()

def search_products_by_name():
    try:
        transaction_cursor = db_connection.cursor()

        # Start transaction
        transaction_cursor.execute("START TRANSACTION")

        product_name = input("Enter the product name you want to search: ")
        query = f"SELECT * FROM product WHERE product_name LIKE '%{product_name}%'"
        transaction_cursor.execute(query)
        products = transaction_cursor.fetchall()

        # Commit the transaction
        db_connection.commit()

        if products:
            print("Products Found:")
            for product in products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Price: {product[3]}")
        else:
            print("No products available with this name.")

    except mysql.connector.Error as err:
        # Rollback the transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        db_connection.rollback()

    finally:
        transaction_cursor.close()

# Transactions added
def view_products(customer_id):
    transaction_cursor = db_connection.cursor()
    try:
        # Start transaction
        transaction_cursor.execute("START TRANSACTION")
        lock_query = "LOCK TABLES products WRITE"
        transaction_cursor.execute(lock_query)

        print("Press 1 to view all products")
        print("Press 2 to view products by category")
        print("Press 3 to search products by name")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            view_all_products()

        elif choice == 2:
            view_products_by_category()

        elif choice == 3:
            search_products_by_name()

        # Commit the transaction
        transaction_cursor.execute("COMMIT")
        print("Transaction committed successfully.")

    except mysql.connector.Error as err:
        # Rollback the transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        transaction_cursor.execute("ROLLBACK")

    finally:
        transaction_cursor.close()
    return

#Used database transactions to ensure that the product is added to the cart only if the quantity is available
def add_to_cart(product_id, quantity, customer_id):
    cpq = check_product_quantity(product_id, quantity)
    transaction_cursor = db_connection.cursor()
    if cpq:
        try:
            transaction_cursor.execute("BEGIN")
            #Check is product is existing, increment its value in the table, otherwise create a separate entry
            query = f"SELECT product_id FROM cart WHERE product_id = {product_id} AND customer_id = {customer_id}"
            transaction_cursor.execute(query)
            result = transaction_cursor.fetchone()
            if result:
                query = f"SELECT * FROM cart WHERE product_id = {product_id} AND customer_id = {customer_id}"
                transaction_cursor.execute(query)
                result1 = transaction_cursor.fetchone()
                current_quantity = result1[2]
                new_quantity = current_quantity + quantity
                query = f"UPDATE cart SET quantity = {new_quantity} WHERE product_id = {product_id} AND customer_id = {customer_id}"
                transaction_cursor.execute(query)
                print("Product added to cart successfully.")
            else:
                price = calculate_price(product_id, quantity)
                query = "INSERT INTO cart (customer_id, product_id, quantity, cost) VALUES (%s, %s, %s, %s)"
                values = (customer_id, product_id, quantity, price)
                db_cursor.execute(query, values)
                print("Product added to cart successfully.")
            db_connection.commit()
        except mysql.connector.Error as error:
            print("Failed to add product to cart.")
            print(f"Error: {error}")
            transaction_cursor.execute("ROLLBACK")
        finally:
            transaction_cursor.close()
    else:
        print("The quantity of the product is greater than the available quantity.")
    return

def check_product_quantity(product_id, quantity):
    query = f"SELECT quantity FROM product WHERE product_id = {product_id}"
    db_cursor.execute(query)
    product_quantity = db_cursor.fetchone()[0]
    return product_quantity >= quantity

def calculate_price(product_id, quantity):
    query = f"SELECT price FROM product WHERE product_id = {product_id}"
    db_cursor.execute(query)
    cost = db_cursor.fetchone()[0]
    return cost * quantity

def add_product_with_inventory():
    try:
        # Start transaction
        transaction_cursor.execute("START TRANSACTION")
        transaction_cursor = db_connection.cursor()
        lock_query = "LOCK TABLES product WRITE"
        transaction_cursor.execute(lock_query)
        lock_query = "LOCK TABLES inventory WRITE"
        transaction_cursor.execute(lock_query)

        # Take input values
        product_name = input("Enter product name: ")
        quantity_product = int(input("Enter quantity in product table: "))
        price = int(input("Enter price: "))
        category_id = int(input("Enter category ID: "))
        quantity_inventory = int(input("Enter quantity in inventory table: "))

        # Insert into product table
        product_insert_query = "INSERT INTO product (product_name, quantity, price, category_id) VALUES (%s, %s, %s, %s)"
        transaction_cursor.execute(product_insert_query, (product_name, quantity_product, price, category_id))
        product_id = transaction_cursor.lastrowid  # Get the ID of the newly inserted product

        # Insert into inventory table
        inventory_insert_query = "INSERT INTO inventory (product_id, quantity) VALUES (%s, %s)"
        transaction_cursor.execute(inventory_insert_query, (product_id, quantity_inventory))

        # Commit transaction
        db_connection.commit()
        print("Product and inventory added successfully.")

    except mysql.connector.Error as err:
        # Rollback transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        db_connection.rollback()

    finally:
        # Close cursor
        unlock_query = "UNLOCK TABLES"
        transaction_cursor.execute(unlock_query)
        transaction_cursor.close()

def delete_product(product_id):
    transaction_cursor = db_connection.cursor()
    try:
        # Start transaction
        transaction_cursor.execute("START TRANSACTION")

        # Lock the product table for writing
        transaction_cursor.execute("LOCK TABLES product WRITE")

        # Delete product
        delete_query = "DELETE FROM product WHERE product_id = %s"
        transaction_cursor.execute(delete_query, (product_id,))

        # Commit transaction
        transaction_cursor.execute("COMMIT")
        print("Product deleted successfully.")

    except mysql.connector.Error as err:
        # Rollback transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        transaction_cursor.execute("ROLLBACK")

    finally:
        # Unlock tables and close cursor
        transaction_cursor.execute("UNLOCK TABLES")
        transaction_cursor.close()

def update_product_details(product_id, new_quantity, new_price):
    transaction_cursor = db_connection.cursor()
    try:
        # Start transaction
        transaction_cursor.execute("START TRANSACTION")

        # Lock the product table for writing
        transaction_cursor.execute("LOCK TABLES product WRITE")

        # Update quantity
        update_quantity_query = "UPDATE product SET quantity = %s WHERE product_id = %s"
        transaction_cursor.execute(update_quantity_query, (new_quantity, product_id))

        # Update price
        update_price_query = "UPDATE product SET price = %s WHERE product_id = %s"
        transaction_cursor.execute(update_price_query, (new_price, product_id))

        # Commit transaction
        transaction_cursor.execute("COMMIT")
        print("Product details updated successfully.")

    except mysql.connector.Error as err:
        # Rollback transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        transaction_cursor.execute("ROLLBACK")

    finally:
        # Unlock tables and close cursor
        transaction_cursor.execute("UNLOCK TABLES")
        transaction_cursor.close()

def manage_products():
    print("Manage Products")
    print("1. Add Product to Inventory")
    print("2. Delete Product")
    print("3. Update Product Details")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        add_product_with_inventory()
    elif choice == 2:
        product_id = int(input("Enter product ID to delete: "))
        delete_product(product_id)
    elif choice == 3:
        product_id = int(input("Enter product ID to update: "))
        new_quantity = int(input("Enter new quantity: "))
        new_price = int(input("Enter new price: "))
        update_product_details(product_id, new_quantity, new_price)
    else:
        print("Invalid option. Please try again.")

def payment_gateway(total_cost):
    print("Payment Gateway")
    print("Please select a payment method:")
    print("1. Credit Card")
    print("2. Debit Card")
    print("3. Net Banking")
    print("4. UPI")
    payment_methods = ["Credit Card", "Debit Card", "Net Banking", "UPI"]
    payment_method = int(input("Enter your choice: "))
    print(f"Payment of Rs {total_cost} successful!")
    query = f"INSERT INTO payment (final_price, payment_method) VALUES ({total_cost}, '{payment_methods[payment_method - 1]}')"
    db_cursor.execute(query)
    db_connection.commit()
    return db_cursor.lastrowid

def clear_cart(customer_id, transaction_cursor):
    try:
        # Clear all items from the cart for the given customer
        query = f"DELETE FROM cart WHERE customer_id = {customer_id}"
        transaction_cursor.execute(query)
        transaction_cursor.execute("COMMIT")
        print("Cart cleared successfully.")
    except Exception as e:
        # Rollback the transaction in case of any exception
        transaction_cursor.execute("ROLLBACK")
        print(f"An error occurred while clearing cart: {str(e)}")

def remove_item_from_cart(customer_id, product_id, transaction_cursor):
    try:
        # Remove a specific item from the cart for the given customer
        query = f"DELETE FROM cart WHERE customer_id = {customer_id} AND product_id = {product_id}"
        transaction_cursor.execute(query)
        transaction_cursor.execute("COMMIT")
        print(f"Item with ID {product_id} removed from cart.")
    except Exception as e:
        # Rollback the transaction in case of any exception
        transaction_cursor.execute("ROLLBACK")
        print(f"An error occurred while removing item from cart: {str(e)}")

def place_order(customer_id, total_cost):
    transaction_cursor = db_connection.cursor()
    try:
        # Begin a database transaction
        transaction_cursor.execute("BEGIN")
        
        # Lock the necessary tables
        lock_query = "LOCK TABLES product WRITE, cart WRITE, customer WRITE, orders WRITE, feedback WRITE, payment WRITE, order_history WRITE"
        transaction_cursor.execute(lock_query)
        
        # Retrieve cart items
        query = f"SELECT product_id, quantity FROM cart WHERE customer_id = {customer_id}"
        transaction_cursor.execute(query)
        cart_items = transaction_cursor.fetchall()
        
        # Check if each item in the cart exists in the products table
        for item in cart_items:
            product_id = item[0]
            
            # Check if we have sufficient quantity of the product the user wants to order
            query = f"SELECT quantity FROM product WHERE product_id = {product_id}"
            transaction_cursor.execute(query)
            product_quantity = transaction_cursor.fetchone()[0]
            query = f"SELECT quantity FROM cart WHERE product_id = {product_id} AND customer_id = {customer_id}"
            transaction_cursor.execute(query)
            cart_quantity = transaction_cursor.fetchone()[0]
            if product_quantity > cart_quantity:
                new_quantity = product_quantity - cart_quantity
                query = f"UPDATE product SET quantity = {new_quantity} WHERE product_id = {product_id}"
                transaction_cursor.execute(query)
            else:
                # Rollback the transaction and remove the item from the cart
                transaction_cursor.execute("ROLLBACK")
                remove_item_from_cart(customer_id, product_id, transaction_cursor)
                print(f"Product with ID {product_id} does not have sufficient quantity. Order failed.")
                return
        
        # Apply membership discount
        query = f"SELECT Membership FROM customer WHERE customer_id = {customer_id}"
        transaction_cursor.execute(query)
        membership = transaction_cursor.fetchone()[0]
        if membership == "Gold":
            total_cost -= total_cost * 0.1
            print("10% discount applied for Gold membership.")
        elif membership == "Basic":
            total_cost -= total_cost * 0.05
            print("5% discount applied for Basic membership.")
        
        # Process payment
        payment_id = payment_gateway(total_cost)
        
        # Commit the transaction
        db_connection.commit()
        print(f"Order placed successfully. Payment ID: {payment_id}")
        
        # Display delivery address
        query = f"SELECT Address FROM customer WHERE customer_id = {customer_id}"
        transaction_cursor.execute(query)
        address = transaction_cursor.fetchone()[0]
        print(f"Order will be delivered to: {address}")
        
        # Insert order details into the orders table
        query = f"INSERT INTO orders (billing_address, final_price, payment_id, customer_id) VALUES ('{address}', {total_cost}, {payment_id}, {customer_id})"
        transaction_cursor.execute(query)
        db_connection.commit()
        
        # Clear the cart
        clear_cart(customer_id, transaction_cursor)
        
    except Exception as e:
        # Rollback the transaction in case of any exception
        transaction_cursor.execute("ROLLBACK")
        print(f"An error occurred: {str(e)}")
        print("Order failed.")
    
    finally:
        # Unlock the tables and close the cursor
        unlock_query = "UNLOCK TABLES"
        transaction_cursor.execute(unlock_query)
        transaction_cursor.close()
    
    return


def view_cart(customer_id):
    query = f"SELECT p.product_name, c.quantity, c.cost FROM cart c JOIN product p ON c.product_id = p.product_id WHERE c.customer_id = {customer_id}"
    db_cursor.execute(query)
    cart_items = db_cursor.fetchall()
    if len(cart_items) > 0:
        total_cost = 0
        for item in cart_items:
            print(f"Product Name: {item[0]}, Quantity: {item[1]}, Cost: {item[2]}")
            total_cost += item[2] * item[1]
        print(f"Total Cost: {total_cost}")
        print()
        print("Do you want to checkout?")
        print("1. Yes")
        print("2. No")
        checkout_choice = int(input("Enter your choice: "))
        if checkout_choice == 1:
            place_order(customer_id, total_cost)
        else:
            return
    else:
        print("No items in the cart.")
    return

def buy_membership(customer_id):
    transaction_cursor = db_connection.cursor()
    try:
        # Start transaction
        transaction_cursor.execute("BEGIN")

        # Check if customer already has a membership
        query_check_membership = f"SELECT Membership FROM customer WHERE customer_id = {customer_id}"
        transaction_cursor.execute(query_check_membership)
        current_membership = transaction_cursor.fetchone()

        if current_membership:
            current_membership = current_membership[0]

            # Check if customer already has a Gold membership
            if current_membership == 'Gold':
                print("You already have a Gold membership. You cannot purchase another membership.")
                return

            # Check if customer has Basic membership
            if current_membership == 'Basic':
                print("You already have a Basic membership.")
                upgrade_choice = input("Do you want to upgrade to Gold membership? (yes/no): ")
                if upgrade_choice.lower() == 'yes':
                    query_upgrade_membership = f"UPDATE customer SET Membership = 'Gold' WHERE customer_id = {customer_id}"
                    payment_gateway(320)  # Assuming the upgrade fee is Rs. 320
                    transaction_cursor.execute(query_upgrade_membership)
                    print("Gold Membership upgraded successfully.")
                    # No need to commit here as it's within the transaction
                else:
                    print("No membership purchased.")
                return

        print("Membership Plans")
        print("1. Basic Membership - Rs 100")
        print("2. Gold Membership - Rs 420")
        print("3. No Membership")
        membership_choice = int(input("Enter your choice: "))

        if membership_choice == 1:
            query = f"UPDATE customer SET Membership = 'Basic' WHERE customer_id = {customer_id}"
            payment_gateway(100)
            transaction_cursor.execute(query)
            print("Basic Membership purchased successfully.")
        elif membership_choice == 2:
            query = f"UPDATE customer SET Membership = 'Gold' WHERE customer_id = {customer_id}"
            payment_gateway(420)
            transaction_cursor.execute(query)
            print("Gold Membership purchased successfully.")
        elif membership_choice == 3:
            print("No Membership purchased.")
        else:
            print("Invalid option. Please try again.")

        # Commit the transaction
        db_connection.commit()
        print("Transaction committed successfully.")

    except mysql.connector.Error as err:
        # Rollback the transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        transaction_cursor.execute("ROLLBACK")
    return

def edit_profile(customer_id):
    transaction_cursor = db_connection.cursor()
    try:
        # Start transaction
        transaction_cursor.execute("BEGIN")

        print("Select an option to edit:")
        print("1. Change Address")
        print("2. Change Email")
        print("3. Change Mobile Number")
        print("4. Change Password")
        print("5. Go back")
        edit_option = int(input("Enter your choice: "))

        if edit_option == 1:
            new_address = input("Enter the new address: ")
            update_address_query = f"UPDATE customer SET Address = '{new_address}' WHERE customer_id = {customer_id}"
            transaction_cursor.execute(update_address_query)
            print("Address updated successfully.")

        elif edit_option == 2:
            new_email = input("Enter the new email: ")
            if not is_valid_email(new_email):
                print("Invalid email address. Please include an '@' in the email address.")
                return
            else:
                update_email_query = f"UPDATE customer SET Email_id = '{new_email}' WHERE customer_id = {customer_id}"
                transaction_cursor.execute(update_email_query)
                print("Email updated successfully.")

        elif edit_option == 3:
            new_mobile = input("Enter the new mobile number: ")
            update_mobile_query = f"UPDATE customer_contact SET contact_number = '{new_mobile}' WHERE customer_id = {customer_id}"
            transaction_cursor.execute(update_mobile_query)
            print("Mobile number updated successfully.")

        elif edit_option == 4:
            old_password = input("Enter the old password: ")
            new_password = input("Enter the new password: ")
            select_password_query = f"SELECT Password FROM customer WHERE customer_id = {customer_id}"
            transaction_cursor.execute(select_password_query)
            result = transaction_cursor.fetchone()
            if result[0] != old_password:
                print("Old password does not match. Please try again.")
                return
            else:
                update_password_query = f"UPDATE customer SET Password = '{new_password}' WHERE customer_id = {customer_id}"
                transaction_cursor.execute(update_password_query)
                print("Password updated successfully.")

        elif edit_option == 5:
            return

        else:
            print("Invalid option. Please try again.")

        # Commit the transaction
        db_connection.commit()

    except mysql.connector.Error as err:
        # Rollback the transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        transaction_cursor.execute("ROLLBACK")
        
    return

def give_feedback(customer_id):
    feedback = input("Enter your feedback: ")
    query = f"INSERT INTO feedback (customer_id, feedback) VALUES ({customer_id}, '{feedback}')"
    db_cursor.execute(query)
    db_connection.commit()
    print("Feedback submitted successfully.")
    return

def customer_menu(customer_id):
    print("Welcome Customer!")
    while True:
        print("Please select an option:")
        customer_option = 0
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Buy Membership")
        print("5. Edit Profile")
        print("6. Give Feedback")
        print("7. Logout")
        customer_option = int(input("Enter your choice: "))
        if customer_option == 1:
            view_products(customer_id)
        elif customer_option == 2:
            add_to_cart_helper(customer_id)
        elif customer_option == 3:
            view_cart(customer_id)
        elif customer_option == 4:
            buy_membership(customer_id)
        elif customer_option == 5:
            edit_profile(customer_id)
        elif customer_option == 6:
            give_feedback(customer_id)
        elif customer_option == 7:
            print("Logging out from Customer account.")
            break
        else:
            print("Invalid option. Please try again.")
    return

def admin_main_menu():
    print("Welcome Admin!")
    while True:
        print("Please select an option:")
        admin_option = 0
        print("1. Login")
        print("2. Exit")
        admin_option = int(input("Enter your choice: "))
        if admin_option == 1:
            admin_login_menu()
        elif admin_option == 2:
            print("Logging out from Admin account.")
            break
        else:
            print("Invalid option. Please try again.")

def customer_main_menu():
    print("Welcome Customer!")
    while True:
        print("Please select an option:")
        customer_option = 0
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        customer_option = int(input("Enter your choice: "))
        if customer_option == 1:
            customer_login_menu()
        elif customer_option == 2:
            customer_signup()
        elif customer_option == 3:
            print("Logging out from Customer account.")
            break
        else:
            print("Invalid option. Please try again.")

## ADMIN FUNCTIONALITIES
        
# Function to fetch top 5 customers based on spending
            
def admin_menu(admin_id):
    print("Welcome Admin!")
    while True:
        print("Please select an option:")
        admin_option = 0
        print("1. View Products")
        print("2. Add Product to Inventory")
        print("3. View Orders")
        print("4. Customer Analytics")
        print("5. Manage Products")
        print("6. View all Suppliers")
        print("7. Manage Admins")
        print("8. Logout")
        admin_option = int(input("Enter your choice: "))
        if admin_option == 1:
            admin_view_products()
        elif admin_option == 2:
            add_product_with_inventory()
        elif admin_option == 3:
            view_orders()
        elif admin_option == 4:
            display_customer_analytics()
        elif admin_option == 5:
            manage_products()
        elif admin_option == 6:
            view_supplier_details()
        elif admin_option == 7:
            manage_admins(admin_id)
        elif admin_option == 8:
            print("Logging out from Admin account.")
            break
        else:
            print("Invalid option. Please try again.")

def admin_view_products():
    transaction_cursor = db_connection.cursor()
    try:
        # Start transaction
        transaction_cursor.execute("START TRANSACTION")

        # Lock the product table for reading
        transaction_cursor.execute("LOCK TABLES product READ")
        
        # Fetch products
        query = "SELECT * FROM product"
        transaction_cursor.execute(query)
        products = transaction_cursor.fetchall()

        # Check if products are available
        if len(products) > 0:
            for product in products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Price: {product[3]}, Quantity: {product[2]}")
        else:
            print("No products available at the moment.")

        # Commit transaction
        transaction_cursor.execute("COMMIT")
        print("Transaction committed successfully.")

    except mysql.connector.Error as err:
        # Rollback transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        transaction_cursor.execute("ROLLBACK")

    finally:
        # Unlock tables and close cursor
        transaction_cursor.execute("UNLOCK TABLES")
        transaction_cursor.close()

    return


def view_orders():
    query = "SELECT * FROM orders"
    db_cursor.execute(query)
    orders = db_cursor.fetchall()
    if len(orders) > 0:
        for order in orders:
            print(f"Order ID: {order[0]}, Address: {order[1]}, Final Price: {order[2]}, Payment ID: {order[3]}, Customer ID: {order[4]}")
    else:
        print("No orders available at the moment.")
    return

def fetch_top_customers():
    query = """
    SELECT c.customer_id, c.customer_name, SUM(o.final_price) AS total_spent
    FROM customer c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_spent DESC
    LIMIT 5
    """
    db_cursor.execute(query)
    top_customers = db_cursor.fetchall()
    return top_customers

# Function to display customer analytics
def display_customer_analytics():
    print("Customer Analytics")
    print("1. Top 5 Customers by Spending")
    print("2. View Customers grouped by age and the average number of orders placed")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        top_customers = fetch_top_customers()
        if top_customers:
            customer_names = [customer[1] for customer in top_customers]
            total_spent = [customer[2] for customer in top_customers]

            # Plotting the bar graph
            plt.bar(customer_names, total_spent)
            plt.xlabel('Customer Name')
            plt.ylabel('Total Spent')
            plt.title('Top 5 Customers Based on Spending')
            plt.xticks(rotation=45)
            plt.show()
        else:
            print("No data available.")
    elif choice == 2:
        query = """
SELECT 
    CASE
        WHEN Age BETWEEN 5 AND 17 THEN '5-17'
        WHEN Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN Age BETWEEN 36 AND 45 THEN '36-45'
        WHEN Age BETWEEN 46 AND 55 THEN '46-55'
        ELSE '55+'
    END AS age_group,
    AVG(order_count) AS avg_orders
FROM (
    SELECT 
        c.customer_id, 
        c.Age,
        COUNT(o.order_id) AS order_count
    FROM customer c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.Age
) AS customer_order_counts
GROUP BY age_group;
        """
        db_cursor.execute(query)
        customer_age_groups = db_cursor.fetchall()
        if customer_age_groups:
            age_groups = [customer_age_group[0] for customer_age_group in customer_age_groups]
            customer_count = [customer_age_group[1] for customer_age_group in customer_age_groups]
            #Make a pie-chart
            plt.pie(customer_count, labels=age_groups, autopct='%1.1f%%')
            plt.title('Average Orders by Age Group')
            plt.show()
        else:
            print("No data available.")
    else:
        print("Invalid option.")

def add_product_to_inventory():
    # Check if the product is already present in the inventory
    query = "SELECT product_id, product_name FROM product"
    db_cursor.execute(query)
    products = db_cursor.fetchall()
    print("List of products:")
    for product in products:
        print(f"Product ID: {product[0]}, Name: {product[1]}")
    product_id = int(input("Enter the product ID: "))
    quantity = int(input("Enter the quantity to be added: "))
    query = "SELECT quantity FROM inventory WHERE product_id = %s"
    db_cursor.execute(query, (product_id,))
    result = db_cursor.fetchone()
    if result:
        quantity += result[0]
        update_query = "UPDATE inventory SET quantity = %s WHERE product_id = %s"
        db_cursor.execute(update_query, (quantity, product_id))
        db_connection.commit()
        print("Product quantity updated successfully.")
    else:
        print("Product does not exist in the inventory.")

    db_cursor.close()
    
def view_supplier_details():
    try:
        # Execute SQL query to select all supplier details
        query = "SELECT * FROM supplier"
        db_cursor.execute(query)

        # Fetch all rows
        supplier_details = db_cursor.fetchall()

        # Print supplier details
        print("Supplier Details:")
        for supplier in supplier_details:
            print(f"Supplier ID: {supplier[0]}")
            print(f"Supplier Name: {supplier[1]}")
            print(f"Contact Number: {supplier[2]}")
            print("----------------------")

    except mysql.connector.Error as err:
        print("Error:", err)

def manage_admins(admin_id):
    print("Admin Management")
    print("1. Add Admin")
    print("2. Update Admin")
    print("3. Delete Admin")
    admin_option = int(input("Enter your choice: "))
    if admin_option == 1:
        add_admin()
    elif admin_option == 2:
        admin_id1 = int(input("Enter admin ID to update: "))
        update_admin(admin_id1)
    elif admin_option == 3:
        admin_id1 = int(input("Enter admin ID to delete: "))
        delete_admin(admin_id1, admin_id)
    else:
        print("Invalid option. Please try again.")

def delete_admin(admin_id1, admin_id):
    try:
        # Start transaction
        transaction_cursor = db_connection.cursor()

        # Begin transaction
        transaction_cursor.execute("START TRANSACTION")
        lock_query = "LOCK TABLES admin WRITE"
        transaction_cursor.execute(lock_query)

        # Check if admin is trying to delete themselves
        check_query = "SELECT admin_id FROM admin WHERE admin_id = %s"
        transaction_cursor.execute(check_query, (admin_id1,))
        result = transaction_cursor.fetchone()

        if result[0] == admin_id:
            print("An admin cannot delete themselves. Rolling back transaction.")
            transaction_cursor.execute("ROLLBACK")
            return

        # Delete admin
        delete_query = "DELETE FROM admin WHERE admin_id = %s"
        transaction_cursor.execute(delete_query, (admin_id1,))

        # Commit transaction
        transaction_cursor.execute("COMMIT")
        print("Admin deleted successfully.")

    except mysql.connector.Error as err:
        # Rollback transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        transaction_cursor.execute("ROLLBACK")

    finally:
        # Close cursor and connection
        unlock_query = "UNLOCK TABLES"
        transaction_cursor.execute(unlock_query)
        transaction_cursor.close()


def update_admin(admin_id):
    try:
        transaction_cursor = db_connection.cursor()
        transaction_cursor.execute("START TRANSACTION")
        lock_query = "LOCK TABLES admin WRITE"
        transaction_cursor.execute(lock_query)

        # Take input choice
        print("Choose which detail to update:")
        print("1. Admin Name")
        print("2. Age")
        print("3. Address")
        print("4. Email")
        print("5. Password")
        choice = int(input("Enter your choice: "))

        # Take input value based on choice
        if choice == 1:
            new_value = input("Enter new admin name: ")
            update_query = "UPDATE admin SET admin_name = %s WHERE admin_id = %s"
        elif choice == 2:
            new_value = int(input("Enter new age: "))
            update_query = "UPDATE admin SET Age = %s WHERE admin_id = %s"
        elif choice == 3:
            new_value = input("Enter new address: ")
            update_query = "UPDATE admin SET Address = %s WHERE admin_id = %s"
        elif choice == 4:
            new_value = input("Enter new email: ")
            update_query = "UPDATE admin SET Email_id = %s WHERE admin_id = %s"
        elif choice == 5:
            new_value = input("Enter new password: ")
            update_query = "UPDATE admin SET Password = %s WHERE admin_id = %s"
        else:
            print("Invalid choice. Rolling back the transaction.")
            transaction_cursor.execute("ROLLBACK")
            return

        # Execute update query
        transaction_cursor.execute(update_query, (new_value, admin_id))

        # Commit transaction
        transaction_cursor.execute("COMMIT")
        print("Admin details updated successfully.")

    except mysql.connector.Error as err:
        # Rollback transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        transaction_cursor.execute("ROLLBACK")

    finally:
        # Close cursor and connection
        unlock_query = "UNLOCK TABLES"
        transaction_cursor.execute(unlock_query)
        transaction_cursor.close()

def add_admin():
    try:
        # Start transaction
        transaction_cursor = db_connection.cursor()
        lock_query = "LOCK TABLES admin WRITE"
        transaction_cursor.execute(lock_query)

        # Begin transaction
        transaction_cursor.execute("START TRANSACTION")

        # Take input values
        admin_name = input("Enter admin name: ")
        age = int(input("Enter age: "))
        address = input("Enter address: ")
        email_id = input("Enter email: ")
        password = input("Enter password: ")

        # Insert into admin table
        admin_insert_query = "INSERT INTO admin (admin_name, Age, Address, Email_id, Password) VALUES (%s, %s, %s, %s, %s)"
        transaction_cursor.execute(admin_insert_query, (admin_name, age, address, email_id, password))

        # Commit transaction
        transaction_cursor.execute("COMMIT")
        print("Admin added successfully.")

    except mysql.connector.Error as err:
        # Rollback transaction if any error occurs
        print("Error:", err)
        print("Rolling back the transaction.")
        transaction_cursor.execute("ROLLBACK")

    finally:
        # Close cursor and connection
        unlock_query = "UNLOCK TABLES"
        transaction_cursor.execute(unlock_query)
        transaction_cursor.close()
    
    return


print("Welcome to FLASH Online Shopping Portal!")
while True:
    print("Please select an option:")
    home_option = 0
    print("1. Enter as Admin")
    print("2. Enter as Customer")
    print("3. Exit")
    home_option = int(input("Enter your choice: "))
    if home_option == 1:
        admin_main_menu()
    elif home_option == 2:
        customer_main_menu()
    elif home_option == 3:
        print("Thank you for visiting FLASH Online Shopping Portal!")
        break
    else:
        print("Invalid option. Please try again.")

# Close the database connection
db_cursor.close()
