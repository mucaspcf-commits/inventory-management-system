# Inventory Management System
# Concepts used: variables, input/output, if/elif/else, loops, functions,
# lists, dictionaries, CSV files and exception handling.
# Import Python's CSV tools so inventory records can be stored in a
# spreadsheet-friendly file.
import csv
# The CSV file will be created in the project folder.
# Name the CSV file used to keep the inventory between runs.
DATA_FILE = "inventory_data.csv"
# Start the ordered list of columns that every inventory record will use.
FIELD_NAMES = [
    # Store the unique identifier in the first CSV column.
    "product_id",
    # Store each product's name in the next column.
    "name",
    # Store the product category in the next column.
    "category",
    # Store the number of units currently available.
    "quantity",
    # Store the price of one unit.
    "price",
    # Store the quantity at which the product needs restocking.
    "reorder_level"
]

# Define the routine that writes the current product list to disk.
def save_inventory(inventory):
    # Document what this function provides to its callers.
    """Save the current inventory in the CSV file."""
    # Try the operation so a recoverable error can be handled below.
    try:
        # Open the CSV for writing, preserving CSV line endings and UTF-8 text.
        with open(DATA_FILE, "w", newline="", encoding="utf-8-sig") as file:
            # Create a writer that maps product dictionary keys
            # to the chosen columns.
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            # Write the CSV column headings before the product rows.
            writer.writeheader()
            # Write one CSV row for each product in memory.
            writer.writerows(inventory)
        # Finish this action and return to its caller.
        return True
    # Handle an operating-system error while accessing the CSV file.
    except IOError:
        # Show this message to the user.
        print("The inventory file could not be saved.")
        # Finish this action and return to its caller.
        return False
# Define the routine that rebuilds the product list from the CSV file.
def load_inventory():
    # Document what this function provides to its callers.
    """Load the inventory from the CSV file."""
    # Start with an empty product list.
    inventory = []
    # Try the operation so a recoverable error can be handled below.
    try:
        # Open the saved CSV for reading with the same text encoding.
        with open(DATA_FILE, "r", newline="", encoding="utf-8-sig") as file:
            # Read each CSV row as a dictionary keyed by the column names.
            reader = csv.DictReader(file)
            # Process each product row from the CSV file.
            for row in reader:
                # Values from a CSV are text, so numbers must be converted.
                # Convert the saved quantity from text to an integer.
                row["quantity"] = int(row["quantity"])
                # Convert the saved unit price from text to a decimal number.
                row["price"] = float(row["price"])
                # Convert the saved reorder threshold from text to an integer.
                row["reorder_level"] = int(row["reorder_level"])
                # Add the converted product to the in-memory inventory.
                inventory.append(row)
    # Handle the first run, when the inventory CSV does not exist yet.
    except FileNotFoundError:
        # On the first run, create an empty file with the correct headings.
        save_inventory(inventory)
    # Handle unreadable data, invalid numbers, or missing CSV columns.
    except (IOError, ValueError, KeyError):
        # Show this message to the user.
        print("The inventory file could not be read correctly.")
    # Give the loaded product list back to the caller.
    return inventory
# Define a reusable prompt that requires a nonempty text answer.
def read_text(message):
    # Document what this function provides to its callers.
    """Do not accept an empty answer."""
    # Keep prompting until this loop reaches a valid return.
    while True:
        # Ask the user for text and remove spaces around the answer.
        value = input(message).strip()
        # Accept the answer only if it contains some text.
        if value != "":
            # Return the validated answer to the calling action.
            return value

        # Show this message to the user.
        print("The value cannot be empty.")


# Define a prompt for whole numbers that meet a minimum value.
def read_integer(message, minimum):
    # Document what this function provides to its callers.
    """Read a valid whole number."""
    # Keep prompting until this loop reaches a valid return.
    while True:
        # Try to convert the input to a whole number.
        try:
            # Ask for input and attempt to convert it to a whole number.
            value = int(input(message))

            # Check if the input is within the minimum.
            if value >= minimum:
                # Return the validated answer to the calling action.
                return value
            # Show this message to the user.
            print("The value must be", minimum, "or greater.")
        # Catch text that cannot be converted to the requested number type.
        except ValueError:
            # Show this message to the user.
            print("Enter a valid whole number.")
# Define a prompt for decimal numbers that meet a minimum value.
def read_float(message, minimum):
    # Document what this function provides to its callers.
    """Read a valid decimal number."""
    # Keep prompting until this loop reaches a valid return.
    while True:
        # Try the operation so a recoverable error can be handled below.
        try:
            # Ask for input and attempt to convert it to a decimal number.
            value = float(input(message))
            # Check that the entered number meets the allowed minimum.
            if value >= minimum:
                # Return the validated answer to the calling action.
                return value
            # Show this message to the user.
            print("The value must be", minimum, "or greater.")
        # Catch text that cannot be converted to the requested number type.
        except ValueError:
            # Show this message to the user.
            print("Enter a valid number, such as 15.50.")
# Function for looking up a product by product ID.
def find_product(inventory, product_id):
    # Document what this function provides to its callers.
    """Find a product using its ID."""
    # Go through each product in the inventory.
    for product in inventory:
        # Check if the product ID matches.
        if product["product_id"].lower() == product_id.lower():
            # Return the product if it is found.
            return product
    # Return nothing if the product is not found.
    return None
# Function for collecting and saving a new product.
def add_product(inventory):
    # Document what this function provides to its callers.
    """Add a new product to the inventory."""
    # Show the action heading.
    print("\nADD PRODUCT")
    # Ask which product ID this action should use.
    product_id = read_text("Product ID: ").upper()
    # If there is a duplicate product ID, the system blocks it.
    if find_product(inventory, product_id) is not None:
        print("A product with this ID already exists.")
        return
    # Create a new product dictionary.
    product = {
        # Save the normalized ID in the new product record.
        "product_id": product_id,
        # Require a nonempty name for the new product.
        "name": read_text("Product name: "),
        # Require a nonempty category for the new product.
        "category": read_text("Category: "),
        # Read a starting quantity that cannot be negative.
        "quantity": read_integer("Quantity: ", 0),
        # Read a unit price that cannot be negative.
        "price": read_float("Unit price: $", 0),
        # Read a nonnegative threshold for low-stock warnings.
        "reorder_level": read_integer("Low-stock level: ", 0)
    }
    # Add the new product to the product list.
    inventory.append(product)
    # Continue with the success message only if the CSV was saved.
    if save_inventory(inventory):
        print("Product added successfully.")
# Define the function that displays a product and its stock value.
def display_product(product):
    # Document what this function provides to its callers.
    """Show the information for one product."""
    # Calculate the value of this product's available units.
    stock_value = product["quantity"] * product["price"]
    # Display the product information.
    print("-" * 50)
    print("Product ID:", product["product_id"])
    print("Name:", product["name"])
    print("Category:", product["category"])
    print("Quantity:", product["quantity"])
    print("Unit price: $" + format(product["price"], ".2f"))
    print("Low-stock level:", product["reorder_level"])
    print("Stock value: $" + format(stock_value, ".2f"))

# Define the action that displays every product in stock.
def view_products(inventory):
    # Document what this function provides to its callers.
    """Show all products."""
    # Show the action heading.
    print("\nALL PRODUCTS")
    # Check whether there are any products to display.
    if len(inventory) == 0:
        print("The inventory is empty.")
        return
    # Visit each product in the current inventory.
    for product in inventory:
        # Print the details of this product using the shared display format.
        display_product(product)
    # Show the end of the list and the total number of products.
    print("-" * 50)
    print("Total products:", len(inventory))
# Define the search across product IDs, names, and categories.
def search_products(inventory):
    # Document what this function provides to its callers.
    """Search by ID, name or category."""
    # Show the action heading.
    print("\nSEARCH PRODUCTS")
    # Read the search phrase and lowercase it for case-insensitive matching.
    search_text = read_text("Enter ID, name, or category: ").lower()
    # Prepare a list to collect products that match the search.
    matches = []
    # Visit each product in the current inventory.
    for product in inventory:
        # Check for the search phrase anywhere in the product ID.
        id_match = search_text in product["product_id"].lower()
        # Check for the search phrase anywhere in the product name.
        name_match = search_text in product["name"].lower()
        # Check for the search phrase anywhere in the category.
        category_match = search_text in product["category"].lower()
        # Treat a match in any of the three fields as a search result.
        if id_match or name_match or category_match:
            # Keep this matching product for display after the search.
            matches.append(product)
    # Check whether the search found any products.
    if len(matches) == 0:
        print("No matching products were found.")
        return
    # Display each product found by the search.
    for product in matches:
        # Print the details of this product using the shared display format.
        display_product(product)
# Define the action that changes one field on an existing product.
def update_product(inventory):
    # Document what this function provides to its callers.
    """Change one detail of a product."""
    # Show the action heading.
    print("\nUPDATE PRODUCT")
    # Ask which product ID this action should use.
    product_id = read_text("Product ID: ")
    # Find the product record for the entered ID.
    product = find_product(inventory, product_id)
    # Stop if the requested product ID does not exist.
    if product is None:
        print("Product not found.")
        return
    # Display the available update options.
    print("1. Change name")
    print("2. Change category")
    print("3. Change price")
    print("4. Change low-stock level")
    # Read the selected option.
    choice = input("Select an option: ")
    # Handle the selected menu option.
    if choice == "1":
        product["name"] = read_text("New name: ")
    elif choice == "2":
        product["category"] = read_text("New category: ")
    elif choice == "3":
        product["price"] = read_float("New price: $", 0)
    elif choice == "4":
        product["reorder_level"] = read_integer("New low-stock level: ", 0)
    else:
        print("Invalid option.")
        return
    # Continue with the success message only if the CSV was saved.
    if save_inventory(inventory):
        print("Product updated successfully.")
# Define the action for receiving or removing units of stock.
def change_stock(inventory):
    # Document what this function provides to its callers.
    """Add or remove units from the stock."""
    # Show the action heading.
    print("\nCHANGE STOCK")
    # Ask which product ID this action should use.
    product_id = read_text("Product ID: ")
    # Find the product record for the entered ID.
    product = find_product(inventory, product_id)
    # Stop if the requested product ID does not exist.
    if product is None:
        print("Product not found.")
        return
    # Show the current stock quantity.
    print("Current quantity:", product["quantity"])
    # Display stock movement options.
    print("1. Stock in")
    print("2. Stock out")
    # Read the selected option.
    choice = input("Select an option: ")
    # Add units to the stock.
    if choice == "1":
        # Ask for a positive number of units to move.
        amount = read_integer("Quantity received: ", 1)
        # Update the product's available unit count.
        product["quantity"] = product["quantity"] + amount
    # Remove units from the stock.
    elif choice == "2":
        # Ask for a positive number of units to move.
        amount = read_integer("Quantity removed: ", 1)
        # Refuse to remove more units than are currently in stock.
        if amount > product["quantity"]:
            print("There is not enough stock.")
            return
        # Update the product's available unit count.
        product["quantity"] = product["quantity"] - amount
    else:
        print("Invalid option.")
        return
    # Continue with the success message only if the CSV was saved.
    if save_inventory(inventory):
        print("Stock updated successfully.")
# Create a report of products at or below their reorder level.
def low_stock_report(inventory):
    # Document what this function provides to its callers.
    """Show products that need restocking."""
    # Display the report heading.
    print("\nLOW-STOCK REPORT")
    # Create a list of products that need restocking.
    low_stock_products = []
    # Check each product in the current inventory.
    for product in inventory:
        # Identify products that have reached the reorder level.
        if product["quantity"] <= product["reorder_level"]:
            # Include this product in the low-stock report.
            low_stock_products.append(product)
    # Verify that all products are above their reorder level.
    if len(low_stock_products) == 0:
        print("No products are low in stock.")
        return
    # Show all items requiring restocking.
    for product in low_stock_products:
        # Display this product's details using the standard format.
        display_product(product)
# Create the action that removes a product after confirmation.
def remove_product(inventory):
    # Document what this function provides to its callers.
    """Remove an inventory item once confirmed."""
    # Display the action heading.
    print("\nREMOVE PRODUCT")
    # Ask for the ID of the product to process.
    product_id = read_text("Product ID: ")
    # Locate the product record using the entered ID.
    product = find_product(inventory, product_id)
    # Exit if the entered product ID is not found.
    if product is None:
        print("Product not found.")
        return
    # Ask for confirmation and convert the reply to uppercase.
    confirmation = input("Type Y to confirm removal: ").strip().upper()
    # Remove the product only when the user enters Y.
    if confirmation == "Y":
        # Delete the selected product from the current inventory list.
        inventory.remove(product)
        # Continue only when the CSV file has been saved successfully.
        if save_inventory(inventory):
            print("Product removed successfully.")
    # Handle the remaining choice or invalid input in this branch.
    else:
        print("Removal cancelled.")
# Define the report of product count, unit count, and total stock value.
def inventory_summary(inventory):
    # Document what this function provides to its callers.
    """Show the main inventory totals."""
    # Display the inventory summary heading.
    print("\nINVENTORY SUMMARY")
    # Start the unit count at zero before totaling all products.
    total_units = 0
    # Start the total inventory value at zero.
    total_value = 0.0
    # Visit each product in the current inventory.
    for product in inventory:
        # Add this product's units to the running total.
        total_units = total_units + product["quantity"]
        # Add this product's stock value to the running total.
        total_value = total_value + product["quantity"] * product["price"]
    # Display the calculated totals.
    print("Different products:", len(inventory))
    print("Total units:", total_units)
    print("Total inventory value: $" + format(total_value, ".2f"))
# Define the menu that lists all available actions.
def display_menu():
    # Document what this function provides to its callers.
    """Show the program menu."""
    # Display the main program menu.
    print("\n" + "=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Add product")
    print("2. View all products")
    print("3. Search products")
    print("4. Update product")
    print("5. Change stock")
    print("6. Low-stock report")
    print("7. Remove product")
    print("8. Inventory summary")
    print("9. Exit")

# Define the main loop that keeps the program running until exit.
def main():
    # Document what this function provides to its callers.
    """Run the program until the user chooses Exit."""
    # Load saved products before showing the main menu.
    inventory = load_inventory()
    # Keep prompting until the user chooses to exit.
    while True:
        # Show the available actions at the start of each menu cycle.
        display_menu()
        # Read the menu number chosen by the user.
        choice = input("Select an option from 1 to 9: ")
        # Run the selected menu option.
        if choice == "1":
            add_product(inventory)
        elif choice == "2":
            view_products(inventory)
        elif choice == "3":
            search_products(inventory)
        elif choice == "4":
            update_product(inventory)
        elif choice == "5":
            change_stock(inventory)
        elif choice == "6":
            low_stock_report(inventory)
        elif choice == "7":
            remove_product(inventory)
        elif choice == "8":
            inventory_summary(inventory)
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print( "Invalid option. Enter a number from 1 to 9." )
# Run the menu only when this file is started directly.
if __name__ == "__main__":
    # Start the inventory program.
    main()