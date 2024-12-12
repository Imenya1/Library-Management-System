import os
import tkinter as tk
from tkinter import messagebox
import psycopg2
from PIL import Image, ImageTk  # For image handling


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("650x550")
        self.root.resizable(False,False)
        
        # Add background image
        self.setup_background_image()

        # Check and set application icon
        icon_path = "icon.png"  # Replace with the correct path to your icon file
        if os.path.exists(icon_path):
            self.icon_image = Image.open(icon_path)
            self.icon_photo = ImageTk.PhotoImage(self.icon_image)
            self.root.iconphoto(False, self.icon_photo)
        else:
            print(f"Icon file '{icon_path}' not found. Defaulting to no icon.")

        # Database connection setup
        self.conn = psycopg2.connect(
            dbname="Library_db", user="postgres", password="3096", host="localhost", port="5432"
        )
        self.cursor = self.conn.cursor()
        self.current_user = None  # Store logged-in user information
        self.animation_text = None  # Store reference to animated text
        self.text_position = 0  # Position of the animated text

        self.show_welcome_page()

    def setup_background_image(self):
        """Setup the background image for the application."""
        try:
            bg_image_path = "backgroundc.png"  # Replace with your background image path
            bg_image = Image.open(bg_image_path).resize((650, 550), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.root.configure(bg="lightgreen")  # Fallback background color

    def clear_window(self):
        """Clears the main window but keeps the background."""
        for widget in self.root.winfo_children():
            if widget != self.bg_label:  # Keep the background image
                widget.destroy()

    def show_welcome_page(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to the Library Management System", font=("Helvetica", 20, "bold"), bg="darkgreen", padx=30 , pady = 20, fg = "gold").pack(pady=(0,170))
        tk.Button(self.root, text="Login", font=("Helvetica", 12, "bold"), fg= 'black', bg = "gold",  width=15, command=self.show_login_page).pack(pady=10)
        tk.Button(self.root, text="Register", font=("Helvetica", 12,"bold"), fg= 'white', bg = "darkgreen", width=15, command=self.show_register_page).pack(pady=10)

    def show_login_page(self):
        self.clear_window()
        self.animation_text = tk.Label(self.root, text="", font=("Helvetica", 20, "italic", "bold"), fg="black", bg="#f1c40f", pady = 20, padx = 225)
        self.animation_text.pack(pady= (0, 60))
        self.text_position = 0  # Reset text position
        self.animate_text("Welcome Back!")
        tk.Label(self.root, text="Username:", fg= 'white', bg="darkgreen").pack(pady=8)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:",fg= 'white',  bg="darkgreen").pack(pady=8)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=8)
        tk.Button(self.root, text="Login", font= (12), command=self.login_user, bg= 'darkblue', fg = "white").pack(pady=10)
        tk.Button(self.root, text="Back to Main Page",font= (12), bg='red', fg= 'white',command=self.show_welcome_page).pack(pady=0)

    def animate_text(self, text):
        if self.animation_text:
            self.animation_text.config(text=text[:self.text_position + 1])
            self.text_position += 1
            if self.text_position <= len(text):
                self.root.after(200, lambda: self.animate_text(text))

    def show_register_page(self):
        self.clear_window()
        tk.Label(self.root, text="Register", bg="darkgreen", fg = 'gold', font=("Helvetica", 16)).pack(pady=20)
        tk.Label(self.root, text="Username:" ,bg="darkgreen", fg= 'white').pack(pady=5)
        self.reg_username_entry = tk.Entry(self.root)
        self.reg_username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:", bg="darkgreen", fg= 'white').pack(pady=5)
        self.reg_password_entry = tk.Entry(self.root, show="*")
        self.reg_password_entry.pack(pady=5)
        tk.Label(self.root, text="Role (admin/member):", bg="darkgreen", fg= 'white').pack(pady=5)
        self.reg_role_entry = tk.Entry(self.root)
        self.reg_role_entry.pack(pady=5)
        tk.Button(self.root, text="Register",font= (12), bg = 'darkblue', fg= 'white', command=self.register_user).pack(pady=20)
        tk.Button(self.root, text="Back to Main Page", font= (12),bg= 'red', fg= 'white', command=self.show_welcome_page).pack(pady=10)

    def register_user(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        role = self.reg_role_entry.get().lower()

        if not username or not password or role not in ["admin", "member"]:
            messagebox.showerror("Error", "Please fill all fields correctly.")
            return

        try:
            query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (username, password, role))
            self.conn.commit()
            messagebox.showinfo("Success", "User registered successfully.")
            self.show_welcome_page()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        query = "SELECT id, role FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result:
            self.current_user = {"id": result[0], "role": result[1]}
            messagebox.showinfo("Success", f"Logged in as {result[1].capitalize()}")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Main Menu", font=("Helvetica", 20, "bold"), bg = '#f1c40f', pady= 30, padx= 275).pack(pady=(0,40))
        if self.current_user["role"] == "admin":
            tk.Button(self.root, text="Add Book",fg= 'white', bg = 'darkgreen' , font=('bold', 12), command=self.add_book).pack(pady=10)
            tk.Button(self.root, text="Remove Book", font= (12),fg= 'black', bg = '#f1c40f' ,command=self.remove_book).pack(pady=10)
        tk.Button(self.root, text="Borrow Book", font= (12),fg= 'white', bg = 'darkgreen' , command=self.borrow_book).pack(pady=10)
        tk.Button(self.root, text="Return Book",font= (12), fg= 'black', bg = '#f1c40f' ,command=self.return_book).pack(pady=10)
        tk.Button(self.root, text="Search Books" ,font= (12),fg= 'white', bg = 'darkgreen' , command=self.search_books).pack(pady=10)
        tk.Button(self.root, text="Logout", font= (12),fg= 'black', bg = '#f1c40f' , command=self.show_welcome_page).pack(pady=20)

    def add_book(self):
        self.show_input_window("Add Book", ["ISBN", "Title", "Author", "Total Copies"], self.process_add_book)

    def process_add_book(self, entries, window):
        isbn = entries["ISBN"].get()
        title = entries["Title"].get()
        author = entries["Author"].get()
        total_copies = entries["Total Copies"].get()

        try:
            query = "INSERT INTO books (isbn, title, author, total_copies, available_copies) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (isbn, title, author, int(total_copies), int(total_copies)))
            self.conn.commit()
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def remove_book(self):
        self.show_input_window("Remove Book", ["ISBN"], self.process_remove_book)

    def process_remove_book(self, entries, window):
        isbn = entries["ISBN"].get()

        try:
            query = "DELETE FROM books WHERE isbn = %s"
            self.cursor.execute(query, (isbn,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Book with ISBN {isbn} removed successfully!")
            else:
                messagebox.showerror("Error", f"No book found with ISBN {isbn}.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def borrow_book(self):
        self.show_input_window("Borrow Book", ["ISBN"], self.process_borrow_book)

    def process_borrow_book(self, entries, window):
        isbn = entries["ISBN"].get()
        query = "UPDATE books SET available_copies = available_copies - 1 WHERE isbn = %s AND available_copies > 0"
        self.cursor.execute(query, (isbn,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            self.cursor.execute("SELECT available_copies FROM books WHERE isbn = %s", (isbn,))
            remaining = self.cursor.fetchone()[0]
            if remaining <= 5:
                messagebox.showwarning("Low Stock", f"Low stock: only {remaining} copies remaining!")
            else:
                messagebox.showinfo("Success", f"Borrowed book with ISBN {isbn} successfully.")
            window.destroy()
        else:
            messagebox.showerror("Error", f"Book with ISBN {isbn} is out of stock.")

    def return_book(self):
        self.show_input_window("Return Book", ["ISBN"], self.process_return_book)

    def process_return_book(self, entries, window):
        isbn = entries["ISBN"].get()
        query = "UPDATE books SET available_copies = available_copies + 1 WHERE isbn = %s"
        self.cursor.execute(query, (isbn,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            messagebox.showinfo("Success", f"Returned book with ISBN {isbn} successfully.")
            window.destroy()
        else:
            messagebox.showerror("Error", f"No book found with ISBN {isbn}.")

    def search_books(self):
        self.show_input_window("Search Books", ["Keyword"], self.process_search_books)

    def process_search_books(self, entries, window):
        keyword = entries["Keyword"].get()
        query = "SELECT isbn, title, author, available_copies FROM books WHERE isbn LIKE %s OR title LIKE %s OR author LIKE %s"
        self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        results = self.cursor.fetchall()

        if results:
            results_window = tk.Toplevel(self.root)
            results_window.title("Search Results")
            for i, (isbn, title, author, available_copies) in enumerate(results, start=1):
                tk.Label(results_window, text=f"{i}. ISBN: {isbn}, Title: {title}, Author: {author}, Copies: {available_copies}").pack(pady=5)
        else:
            messagebox.showinfo("No Results", f"No books found matching '{keyword}'.")
        window.destroy()

    def show_input_window(self, title, labels, process_func):
        window = tk.Toplevel(self.root)
        window.title(title)
        entries = {}
        for label in labels:
            tk.Label(window, text=label).pack(pady=5)
            entry = tk.Entry(window)
            entry.pack(pady=5)
            entries[label] = entry
        tk.Button(window, text="Submit", command=lambda: process_func(entries, window)).pack(pady=10)

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
