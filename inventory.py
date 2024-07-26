"""
Program Name: ICS3UI Final Summative 
Programmer Name: Luna Gao 
Program Date: June 14, 2023         
Program Description: An inventory management app for a sports merchandising business  
Program Input/output:
Input: Product name and stock quantity 
       Choose to perform actions such as adding a product, saving products to a file, displaying products, searching for products, and sorting products
Output: Messages in the GUI text widget for feedback on actions such as adding a product, saving to file, removing a product, updating stock, and searching for products.
        Details of products in the GUI text widget when displaying products or performing a search.
        Message box to show information when a product is removed or the stock is updated.
"""

#Import the tkinter module for GUI
import tkinter as tk
#Import the messagebox module from tkinter for displaying message boxes
from tkinter import messagebox

#Define a Product class
class Product:
    def __init__(self, name, stock):
        #Initialize the product name
        self.name = name
        #Initialize the product stock
        self.stock = stock
    
    def update_stock(self, new_stock):
        #Update the product stock with a new value
        self.stock = new_stock

    def display_details(self):
        #Return a formatted string with product details
        return f"Product: {self.name}\nStock: {self.stock}"

#Define a ProductManagementApp class
class ProductManagementApp:
    def __init__(self):
        #Initialize an empty list to store products
        self.products = []

        #Create the main Tkinter window
        self.root = tk.Tk()
        #Set the title of the window
        self.root.title("Inventory Management")

        #Create and pack GUI elements for product name
        #Create a label for the product name
        self.name_label = tk.Label(self.root, text="Product Name:")
        self.name_label.pack()
        #Create an entry field for entering the product name
        self.name_entry = tk.Entry(self.root, width=20)
        self.name_entry.pack()

        #Create and pack GUI elements for product stock
        #Create a label for the product stock
        self.stock_label = tk.Label(self.root, text="Number in Stock:")
        self.stock_label.pack()
        #Create an entry field for entering the product stock
        self.stock_entry = tk.Entry(self.root, width=20)
        self.stock_entry.pack()

        #Create and pack the "Add Product" button
        self.add_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_button.pack()

        #Create and pack the "Save to File" button
        self.save_button = tk.Button(self.root, text="Save to File", command=self.save_to_file)
        self.save_button.pack()

        #Create and pack the "Display Products" button
        self.display_button = tk.Button(self.root, text="Display Products", command=self.display_products)
        self.display_button.pack()

        #Create and pack the "Sort" button
        self.sort_button = tk.Button(self.root, text="Sort Products", command=self.sort_products)
        self.sort_button.pack()

        #Create and pack GUI elements for search
        #Create a label for the search
        self.search_label = tk.Label(self.root, text="Search:")
        self.search_label.pack()
        #Create an entry field for entering the search keyword
        self.search_entry = tk.Entry(self.root, width=20)
        self.search_entry.pack()

        #Create and pack the search button
        self.search_button = tk.Button(self.root, text="Search", command=self.search_product)
        self.search_button.pack()

        #Create and pack GUI elements for displaying results
        #Create a label for the results
        self.result_label = tk.Label(self.root, text="Results:")
        self.result_label.pack()

        #Create a text area for displaying the product details
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack()

        #Load previously saved products from file
        self.read_from_file() 

        #Start the Tkinter event loop
        self.root.mainloop()

    #Implement the add_product method
    def add_product(self):
        #Get the entered product name
        name = self.name_entry.get()
        #Get the entered product stock
        stock = self.stock_entry.get()

        #Check if the name is empty
        if name == "" or not isinstance(name, str):
            #Show an error message if the name is invalid
            messagebox.showerror("Invalid Input", "Invalid input: Please enter a product name")
        else:
            # Check if the stock is a non-negative integer or float
            if not (stock.isdigit() or self.is_float(stock)) or float(stock) < 0:
                #Show an error message if the stock is invalid
                messagebox.showerror("Invalid Input", "Invalid input: Please enter a proper stock")
            else:
                #Create a new product instance
                product = Product(name, stock)
                #Add the product to the list of products
                self.products.append(product)
                #Display a message indicating the product is added
                self.result_text.insert(tk.END, f"Adding product {name} with stock {stock}\n")
                #Clear the entry fields
                self.clear_entry_fields()

    #Implement the save to file method
    def save_to_file(self):
        #Open a file for writing
        with open('products.txt', 'w') as f:
            for product in self.products:
                #Write each product's details to the file
                f.write(f'{product.name} - {product.stock}\n')

        #Display a message
        self.result_text.insert(tk.END, "Products saved to file\n")

    #Implement the read_from_file method
    def read_from_file(self):
        try:
           #Open the file for reading
            with open('products.txt', 'r') as f:
                for line in f:
                    #Split each line into name and stock
                    name, stock = line.strip().split(' - ')
                    #Create a new Product instance
                    product = Product(name, stock)
                    #Add the product to the list
                    self.products.append(product)
        except FileNotFoundError:
             #Display a message
            self.result_text.insert(tk.END, "No saved products found\n")

    #Implement the display_products method
    def display_products(self):
        #Create a new window
        products_window = tk.Toplevel(self.root)
         #Set the title of the window
        products_window.title("Products")

        #Create a label for selecting a product
        select_label = tk.Label(products_window, text="Select a product")
        select_label.pack()
      
        #Iterate over each product in the list of products
        for product in self.products:
            #Create a label for product details
            product_label = tk.Label(products_window, text=product.display_details())
            product_label.pack()

            #Create and pack the "Remove Product" button
            remove_button = tk.Button(products_window, text="Remove Product", command=lambda p=product: self.remove_product(p, products_window))
            remove_button.pack()

            #Create and pack the "Update Stock" button
            update_button = tk.Button(products_window, text="Update Stock", command=lambda p=product: self.open_update_stock_window(p, products_window))
            update_button.pack()

    #Implement the remove_product method
    def remove_product(self, product, products_window):
        #Remove the product from the list
        self.products.remove(product)
        #Display a message
        self.result_text.insert(tk.END, f"Product {product.name} removed\n")
         #Show info in a message box
        messagebox.showinfo("Product Removed", f"Product {product.name} removed")
        #Close the products window
        products_window.destroy()
      
    #Implement the open_update_stock_window method
    def open_update_stock_window(self, product, products_window):
        #Create a new window
        update_window = tk.Toplevel(products_window)
        #Set the title of the window
        update_window.title("Update Stock")

        #Create a label for entering the new stock
        new_stock_label = tk.Label(update_window, text="New Stock:")
        new_stock_label.pack()

        #Create an entry field for entering the new stock
        new_stock_entry = tk.Entry(update_window, width=20)
        new_stock_entry.pack()

        #Create and pack the "Confirm" button
        confirm_button = tk.Button(
            update_window,
            text="Confirm",
            command=lambda: self.update_stock(product, new_stock_entry.get(), update_window, products_window),
        )
        confirm_button.pack()

    #Implement the update_stock method
    def update_stock(self, product, new_stock, update_window, products_window):
        #Check if the new_stock is a non-negative integer or float
        if not (new_stock.isdigit() or self.is_float(new_stock)) or float(new_stock) < 0:
            #Show an error message if input is invalid
            messagebox.showerror("Invalid Input", "Invalid input: Please enter a proper stock")
        else:
            #Update the product stock
            product.update_stock(new_stock)
            #Display a message
            self.result_text.insert(tk.END, f"Product {product.name} stock updated to {new_stock}\n")
            #Show info in a message box
            messagebox.showinfo("Stock Updated", f"Product {product.name} stock updated to {new_stock}")
            #Close the update window
            update_window.destroy()
            #Close the products window
            products_window.destroy()

# Helper method to check if a string can be converted to a float
    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    #Implement the clear_entry_fields method
    def clear_entry_fields(self):
        #Clear the name entry field
        self.name_entry.delete(0, tk.END)
        #Clear the stock entry field
        self.stock_entry.delete(0, tk.END)
        #Set the focus back to the name entry field
        self.name_entry.focus_set()

    #Implement the search_product method
    def search_product(self):
        #Get the search keyword
        keyword = self.search_entry.get()
        #Perform case-insensitive search
        search_results = [product for product in self.products if keyword.lower() in product.name.lower()]

        #Clear the result text widget
        self.result_text.delete(1.0, tk.END)
        if search_results:
            for product in search_results:\
                #Display product details
                self.result_text.insert(tk.END, product.display_details() + "\n")
        else:
            #Display a message
            self.result_text.insert(tk.END, "No matching products found\n")

    #Implement the sort_products method
    def sort_products(self):
        #Sort the products list alphabetically
        self.products.sort(key=lambda product: product.name.lower())
        #Clear the result text widget
        self.result_text.delete(1.0, tk.END)
        #Display a message
        self.result_text.insert(tk.END, "Products sorted alphabetically\n")
        for product in self.products:
            #Display product details
            self.result_text.insert(tk.END, product.display_details() + "\n")

if __name__ == '__main__':
    #Create an instance of the ProductManagementApp class and start the application
    app = ProductManagementApp()