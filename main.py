import tkinter as tk
import mysql.connector
from tkinter import ttk
from mysql.connector import Error
from datetime import datetime, timedelta
from tkinter import messagebox
from PIL import ImageTk, Image



def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Your MySQL username
            password="",  # Your MySQL password (leave blank if none)
            database="library_system"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


users = {}
books = [
    {"title": "Peter Pan", "borrowed_by": None, "due_date": None},
    {"title": "English for You and Me", "borrowed_by": None, "due_date": None},
    {"title": "Filipino", "borrowed_by": None, "due_date": None},
    {"title": "Music and Arts", "borrowed_by": None, "due_date": None},
    {"title": "Physical Education", "borrowed_by": None, "due_date": None},
    {"title": "Earth and Science", "borrowed_by": None, "due_date": None},
    {"title": "Fundamentals of ABM", "borrowed_by": None, "due_date": None},
    {"title": "ESP", "borrowed_by": None, "due_date": None},
]

root = tk.Tk()
root.title("CPNHS Digital Library System")
root.geometry("1000x900")
root.configure(bg='white')

current_user = None

message_label = tk.Label(root, bg='white', font=("Arial", 12))
message_label.pack(pady=5)


def clear_window():
    for widget in root.winfo_children():
        if widget != message_label:
            widget.destroy()


def register_user():
    username = entry_username.get()
    password = entry_password.get()
    firstname = entry_firstname.get()
    lastname = entry_lastname.get()
    age = entry_age.get()

    if username and password and firstname and lastname and age:
        try:
            age = int(age)  # Ensure age is a number
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age.")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Check if the username already exists
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                if result:
                    messagebox.showerror("Error", "Username already exists!")
                else:
                    # Insert new user into the database
                    query = "INSERT INTO users (username, password, firstname, lastname, age) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (username, password, firstname, lastname, age))
                    conn.commit()

                    messagebox.showinfo("Success", "User registered successfully!")
            except Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")
    else:
        messagebox.showinfo("Caution!!", "Please fill in all fields!")


def login_user():
    global current_user, current_firstname

    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        # Connect to MySQL database
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT username, firstname FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()

                if result:
                    current_user = result[0]
                    current_firstname = result[1]
                    open_main_menu()
                else:
                    messagebox.showerror("Error", "Invalid username or password!")
            except Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")
    else:
        messagebox.showinfo("Caution", "Please enter both username and password.")


def show_login():
    clear_window()
    root.state('normal')

    root.configure(bg='white')
    # Load and place the image on the left side
    img = Image.open("assets/background.png")
    img = img.resize((300, 900), Image.ANTIALIAS)  # Resize image to fit the left side
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.place(x=0, y=0, width=300, height=900)

    # Load icons for username and password fields
    username_icon = tk.PhotoImage(file="assets/user.png")  # Replace with your own icon path
    password_icon = tk.PhotoImage(file="assets/key.png")  # Replace with your own icon path

    # Right side Login form
    login_frame = tk.Frame(root, bg='white')
    login_frame.place(x=400, y=200, width=700, height=900)

    # Login Title
    login_label = tk.Label(login_frame, text="Login", font=("Arial", 24, "bold"), bg='white', fg='gray')
    login_label.place(x=180, y=50)

    # Username field with icon
    username_icon_label = tk.Label(login_frame, image=username_icon, bg='white', fg='gray')
    username_icon_label.image = username_icon  # Keep a reference to avoid garbage collection
    username_icon_label.place(x=50, y=180)

    username_label = tk.Label(login_frame, text="Username", font=("Arial", 14), bg='white', fg='gray')
    username_label.place(x=100, y=150)

    global entry_username
    entry_username = tk.Entry(login_frame, width=25, font=("Arial", 14), bg='white', fg='gray')
    entry_username.place(x=100, y=180)

    # Password field with icon
    password_icon_label = tk.Label(login_frame, image=password_icon, bg='white')
    password_icon_label.image = password_icon  # Keep a reference to avoid garbage collection
    password_icon_label.place(x=50, y=260)

    password_label = tk.Label(login_frame, text="Password", font=("Arial", 14), bg='white', fg='gray')
    password_label.place(x=100, y=230)

    global entry_password
    entry_password = tk.Entry(login_frame, show="*", width=25, font=("Arial", 14), bg='white', fg='gray')
    entry_password.place(x=100, y=260)

    # Login button
    login_btn = tk.Button(login_frame, text="LOGIN", command=login_user, bg='#007BFF', fg='white',
                          font=("Arial", 14, "bold"), cursor="hand2")
    login_btn.place(x=100, y=320, width=280, height=40)

    # Register button
    register_btn = tk.Button(login_frame, text="Create an account", command=show_register, bg='lightgrey',
                             font=("Arial", 12), cursor="hand2")
    register_btn.place(x=100, y=380, width=280, height=30)


def show_register():
    clear_window()
    # Set the background color of the root window
    root.configure(bg='white')
    # Load and place the image on the left side
    img = Image.open("assets/background.png")
    img = img.resize((300, 900), Image.ANTIALIAS)  # Resize image to fit the left side
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.place(x=0, y=0, width=300, height=900)

    # Create a frame for the registration form
    form_frame = tk.Frame(root, bg='white', padx=20, pady=20)  # Form frame with padding
    form_frame.place(x=400, y=230, width=700, height=900)  # Adjust the position and size of the form

    # Register label
    register_label = tk.Label(form_frame, text="Register", font=("Arial", 24, "bold"), bg='white', fg='gray')
    register_label.grid(row=0, columnspan=2, pady=(0, 20))  # Reduce vertical padding

    # Username and Firstname
    username_label = tk.Label(form_frame, text="Username", font=("Arial", 14), bg='white', fg='gray')
    username_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    global entry_username
    entry_username = tk.Entry(form_frame, width=30, font=("Arial", 14), bg='white', fg='gray')  # Increased width
    entry_username.grid(row=1, column=1, pady=5)

    # Password and Lastname
    password_label = tk.Label(form_frame, text="Password", font=("Arial", 14), bg='white', fg='gray')
    password_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

    global entry_password
    entry_password = tk.Entry(form_frame, show="*", width=30, font=("Arial", 14), bg='white', fg='gray')  # Increased width
    entry_password.grid(row=2, column=1, pady=5)

    firstname_label = tk.Label(form_frame, text="Firstname", font=("Arial", 14), bg='white', fg='gray')
    firstname_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

    global entry_firstname
    entry_firstname = tk.Entry(form_frame, width=30, font=("Arial", 14), bg='white', fg='gray')  # Increased width
    entry_firstname.grid(row=3, column=1, pady=5)

    lastname_label = tk.Label(form_frame, text="Lastname", font=("Arial", 14), bg='white', fg='gray')
    lastname_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')

    global entry_lastname
    entry_lastname = tk.Entry(form_frame, width=30, font=("Arial", 14), bg='white', fg='gray')  # Increased width
    entry_lastname.grid(row=4, column=1, pady=5)

    # Age
    age_label = tk.Label(form_frame, text="Age", font=("Arial", 14), bg='white', fg='gray')
    age_label.grid(row=5, column=0, padx=10, pady=5, sticky='w')

    global entry_age
    entry_age = tk.Entry(form_frame, width=30, font=("Arial", 14), bg='white', fg='gray')  # Increased width
    entry_age.grid(row=5, column=1, pady=5)

    # Role Selection
    role_label = tk.Label(form_frame, text="Role", font=("Arial", 14), bg='white', fg='gray')
    role_label.grid(row=6, column=0, padx=10, pady=5, sticky='w')

    global role_var
    role_var = tk.StringVar(value="student")  # Default value

    # Radio buttons for role selection
    student_radio = tk.Radiobutton(form_frame, text="Student", variable=role_var, value="student", bg='white', fg='gray')
    student_radio.grid(row=6, column=1, sticky='w')

    teacher_radio = tk.Radiobutton(form_frame, text="Teacher", variable=role_var, value="teacher", bg='white', fg='gray')
    teacher_radio.grid(row=7, column=1, sticky='w')

    admin_radio = tk.Radiobutton(form_frame, text="Admin", variable=role_var, value="admin", bg='white', fg='gray')
    admin_radio.grid(row=8, column=1, sticky='w')

    # Create Button
    create_button = tk.Button(form_frame, text="Create", command=register_user, bg='#007BFF', fg='white',
                              font=("Arial", 14, "bold"), cursor="hand2")
    create_button.grid(row=9, column=0, columnspan=2, pady=(20, 10), sticky='ew')  # Centered

    # Back Button
    back_button = tk.Button(form_frame, text="Back", command=show_login, bg='lightgrey', fg='black',
                            font=("Arial", 12), cursor="hand2")
    back_button.grid(row=10, column=0, columnspan=2, pady=(0, 10), sticky='ew')


def open_main_menu():
    clear_window()
    # Maximize the window on opening
    root.state('zoomed')  # Maximize windo

    # Main window configuration
    root.config(bg="white")  # Main window background color

    # Header section (Title)
    header_frame = tk.Frame(root, bg="#333333", height=80)
    header_frame.pack(fill="x", side="top")

    title_label = tk.Label(header_frame, text=f"Welcome, {current_firstname}", fg="white", bg="#333333",
                           font=("Arial", 40, "bold"))
    title_label.pack(side=tk.LEFT, pady=20)  # Align to the LEFT

    # Left-side buttons in a vertical frame
    button_frame = tk.Frame(root, bg="#D3D3D3", width=300)
    button_frame.pack(side="left", fill="y", padx=10, pady=20)

    # Buttons for library functionalities
    view_books_button = tk.Button(button_frame, text="📚 View Books", width=20, command=view_books, font=("Arial", 18), anchor="w", bg="#E0E0E0")
    view_books_button.pack(pady=10, padx=10, fill="x")

    borrow_books_button = tk.Button(button_frame, text="📥 Borrow Books", width=20, command=borrow_books, font=("Arial", 18), anchor="w", bg="#E0E0E0")
    borrow_books_button.pack(pady=10, padx=10, fill="x")

    return_books_button = tk.Button(button_frame, text="📤 Return Books", width=20, command=return_books, font=("Arial", 18), anchor="w", bg="#E0E0E0")
    return_books_button.pack(pady=10, padx=10, fill="x")

    add_books_button = tk.Button(button_frame, text="📖 Add Books", width=20, command=add_books, font=("Arial", 18), anchor="w", bg="#E0E0E0")
    add_books_button.pack(pady=10, padx=10, fill="x")

    log_out_button = tk.Button(button_frame, text="🔒 Logout", width=20, command=show_login, font=("Arial", 18), anchor="w", bg="#E0E0E0")
    log_out_button.pack(pady=10, padx=10, fill="x")

    # Search books section on the top-right
    search_label = tk.Label(root, text="Search Books:", bg="#333333", fg="white", font=("Arial", 18))
    search_label.place(x=1270, y=60)

    book_titles = [book['title'] for book in books]  # List of all book titles
    search_combobox = ttk.Combobox(root, values=book_titles, width=30, font=("Arial", 20))
    search_combobox.place(x=1270, y=90)

    def search_action():
        result = ""
        search_term = search_combobox.get().lower()

        if not search_term:
            messagebox.showerror("Error!!", "Please fill the search bar")
            return  # Stop the function if no input is provided

        for book in books:
            if search_term in book["title"].lower():
                status = "Available" if book["borrowed_by"] is None else f"Borrowed by {book['borrowed_by']}"
                result += f"{book['title']} - {status}\n"

        if result:
            messagebox.showinfo("Search Results", result)
        else:
            messagebox.showerror("Error", "No books found.")

    search_button = tk.Button(root, text="Search", width=10, command=search_action, font=("Arial", 14))
    search_button.place(x=1750, y=90)

    # Status section for borrowed books (Centering horizontally and vertically)
    status_label = tk.Label(root, text="Borrowed Books Status", bg="white", font=("Arial", 20))

    # Calculate center position
    window_width = root.winfo_width()
    status_label_width = 400  # Estimated width of the label
    status_list_width = 500   # Estimated width of the text box

    status_x = (window_width - status_label_width) // 2
    status_y = 250  # Adjusted y position

    status_label.place(x=status_x, y=status_y)

    status_list = tk.Text(root, bg="lightyellow", width=100, height=10, font=("Arial", 14))
    status_list.place(x=(window_width - status_list_width) // 2, y=status_y + 50)  # Adjusting to follow the label

    # Database connection
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT books.title, books.due_date FROM books "
        f"JOIN users ON books.borrowed_by = users.id "
        f"WHERE users.username = '{current_user}'"
    )

    borrowed_books = cursor.fetchall()

    # Display borrowed books and overdue penalties
    for book in borrowed_books:
        title, due_date = book
        days_overdue = (datetime.now().date() - due_date).days if due_date and due_date < datetime.now().date() else 0
        penalty = days_overdue * 25 if days_overdue > 0 else 0
        status_list.insert(tk.END, f"{title} - Due: {due_date}, Penalty: {penalty} pesos\n")

    status_list.config(state=tk.DISABLED)
    connection.close()



def view_books():
    clear_window()
    root.config(bg="white")  # Set main window background color

    # Header section (Title)
    header_frame = tk.Frame(root, bg="#333333", height=80)
    header_frame.pack(fill="x", side="top")

    title_label = tk.Label(header_frame, text=f"Available Books", fg="white", bg="#333333",
                           font=("Arial", 40, "bold"))
    title_label.pack(pady=20)
    # Left-side buttons in a vertical frame
    button_frame = tk.Frame(root, bg="#D3D3D3", width=300)
    button_frame.pack(side="left", fill="y", padx=10, pady=20)

    # Buttons for library functionalities
    view_books_button = tk.Button(button_frame, text="📚 View Books", width=20, command=view_books, font=("Arial", 18),
                                  anchor="w", bg="#E0E0E0")
    view_books_button.pack(pady=10, padx=10, fill="x")

    borrow_books_button = tk.Button(button_frame, text="📥 Borrow Books", width=20, command=borrow_books,
                                    font=("Arial", 18), anchor="w", bg="#E0E0E0")
    borrow_books_button.pack(pady=10, padx=10, fill="x")

    return_books_button = tk.Button(button_frame, text="📤 Return Books", width=20, command=return_books,
                                    font=("Arial", 18), anchor="w", bg="#E0E0E0")
    return_books_button.pack(pady=10, padx=10, fill="x")

    add_books_button = tk.Button(button_frame, text="📖 Add Books", width=20, command=add_books, font=("Arial", 18),
                                 anchor="w", bg="#E0E0E0")
    add_books_button.pack(pady=10, padx=10, fill="x")

    log_out_button = tk.Button(button_frame, text="🔒 Logout", width=20, command=show_login, font=("Arial", 18),
                               anchor="w", bg="#E0E0E0")
    log_out_button.pack(pady=10, padx=10, fill="x")

    # Books list display
    books_list = tk.Text(root, bg='lightyellow', width=50, height=15, font=("Arial", 20))
    books_list.pack(pady=20, padx=10)  # Centered books list with padding

    # Database connection and book listing
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT title, borrowed_by FROM books")
        book_list = cursor.fetchall()

        for title, borrowed_by in book_list:
            status = "Available" if not borrowed_by else "Borrowed"
            books_list.insert(tk.END, f"{title} - {status}\n")

        books_list.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        connection.close()

    # Back button at the bottom
    back_frame = tk.Frame(root, bg='white')
    back_frame.pack(side="bottom", pady=20)  # Positioned at the bottom with padding

    back_button = tk.Button(back_frame, text="Back", command=open_main_menu, font=("Arial", 30))
    back_button.pack(pady=10)  # Centered back button with padding

def borrow_books():
    clear_window()
    root.config(bg="white")  # Set main window background color

    # Header section (Title)
    header_frame = tk.Frame(root, bg="#333333", height=80)
    header_frame.pack(fill="x", side="top")

    title_label = tk.Label(header_frame, text=f"Borrow Books", fg="white", bg="#333333",
                           font=("Arial", 40, "bold"))
    title_label.pack(pady=20)

    # Left-side buttons in a vertical frame
    button_frame = tk.Frame(root, bg="#D3D3D3", width=300)
    button_frame.pack(side="left", fill="y", padx=10, pady=20)

    # Buttons for library functionalities
    view_books_button = tk.Button(button_frame, text="📚 View Books", width=20, command=view_books, font=("Arial", 18),
                                  anchor="w", bg="#E0E0E0")
    view_books_button.pack(pady=10, padx=10, fill="x")

    borrow_books_button = tk.Button(button_frame, text="📥 Borrow Books", width=20, command=borrow_books,
                                    font=("Arial", 18), anchor="w", bg="#E0E0E0")
    borrow_books_button.pack(pady=10, padx=10, fill="x")

    return_books_button = tk.Button(button_frame, text="📤 Return Books", width=20, command=return_books,
                                    font=("Arial", 18), anchor="w", bg="#E0E0E0")
    return_books_button.pack(pady=10, padx=10, fill="x")

    add_books_button = tk.Button(button_frame, text="📖 Add Books", width=20, command=add_books, font=("Arial", 18),
                                 anchor="w", bg="#E0E0E0")
    add_books_button.pack(pady=10, padx=10, fill="x")

    log_out_button = tk.Button(button_frame, text="🔒 Logout", width=20, command=show_login, font=("Arial", 18),
                               anchor="w", bg="#E0E0E0")
    log_out_button.pack(pady=10, padx=10, fill="x")

    # Available books list display
    books_listbox = tk.Listbox(root, bg='lightyellow', width=50, height=15, font=("Arial", 20))
    books_listbox.pack(pady=20, padx=10)  # Centered listbox with padding

    # Database connection and fetching available books
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT title FROM books WHERE borrowed_by IS NULL")
        available_books = cursor.fetchall()

        # Populate the listbox with available books
        for book in available_books:
            books_listbox.insert(tk.END, book[0])  # book[0] contains the title
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        connection.close()

    def borrow_selected():
        connection = connect_to_db()
        cursor = connection.cursor()

        selected_index = books_listbox.curselection()

        if selected_index:
            selected_book = books_listbox.get(selected_index)

            cursor.execute("SELECT id FROM users WHERE username = %s", (current_user,))
            user_id = cursor.fetchone()[0]

            # Update book's borrowed_by and due_date in the database
            cursor.execute(
                "UPDATE books SET borrowed_by = %s, due_date = %s WHERE title = %s AND borrowed_by IS NULL",
                (user_id, (datetime.now() + timedelta(days=7)).date(), selected_book)
            )

            if cursor.rowcount > 0:
                connection.commit()
                messagebox.showinfo("Success", f"You have borrowed '{selected_book}'. Due date is {datetime.now() + timedelta(days=7)}")
            else:
                messagebox.showerror("Error", f"The book '{selected_book}' is already borrowed.")
        else:
            messagebox.showerror("Error", "Please select a book before clicking Borrow.")

        connection.close()
        borrow_books()  # Refresh the view

    # Bottom frame for Borrow and Back buttons
    bot_frame = tk.Frame(root, bg='white')
    bot_frame.pack(side="bottom", pady=20)  # Positioned at the bottom with padding

    borrow_button = tk.Button(bot_frame, text="Borrow", command=borrow_selected, font=("Arial", 30))
    borrow_button.pack(pady=10)  # Centered borrow button with padding

    back_button = tk.Button(bot_frame, text="Back", command=open_main_menu, font=("Arial", 30))
    back_button.pack(pady=10)  # Centered back button with padding


def return_books():
    clear_window()
    root.config(bg="white")  # Set main window background color

    # Header section (Title)
    header_frame = tk.Frame(root, bg="#333333", height=80)
    header_frame.pack(fill="x", side="top")

    title_label = tk.Label(header_frame, text=f"Return Books", fg="white", bg="#333333",
                           font=("Arial", 40, "bold"))
    title_label.pack(pady=20)

    # Left-side buttons in a vertical frame
    button_frame = tk.Frame(root, bg="#D3D3D3", width=300)
    button_frame.pack(side="left", fill="y", padx=10, pady=20)

    # Buttons for library functionalities
    view_books_button = tk.Button(button_frame, text="📚 View Books", width=20, command=view_books, font=("Arial", 18),
                                  anchor="w", bg="#E0E0E0")
    view_books_button.pack(pady=10, padx=10, fill="x")

    borrow_books_button = tk.Button(button_frame, text="📥 Borrow Books", width=20, command=borrow_books,
                                    font=("Arial", 18), anchor="w", bg="#E0E0E0")
    borrow_books_button.pack(pady=10, padx=10, fill="x")

    return_books_button = tk.Button(button_frame, text="📤 Return Books", width=20, command=return_books,
                                    font=("Arial", 18), anchor="w", bg="#E0E0E0")
    return_books_button.pack(pady=10, padx=10, fill="x")

    add_books_button = tk.Button(button_frame, text="📖 Add Books", width=20, command=add_books, font=("Arial", 18),
                                 anchor="w", bg="#E0E0E0")
    add_books_button.pack(pady=10, padx=10, fill="x")

    log_out_button = tk.Button(button_frame, text="🔒 Logout", width=20, command=show_login, font=("Arial", 18),
                               anchor="w", bg="#E0E0E0")
    log_out_button.pack(pady=10, padx=10, fill="x")

    # Fetch the user ID from the database
    connection = connect_to_db()  # Reuse this connection
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (current_user,))
    user_id = cursor.fetchone()[0]

    # Show books borrowed by the current user based on user ID
    books_listbox = tk.Listbox(root, width=50, height=15, bg='lightyellow', font=("Arial", 20))
    books_listbox.pack(pady=20, padx=10)  # Centered listbox with padding

    cursor.execute("SELECT title FROM books WHERE borrowed_by = %s", (user_id,))
    borrowed_books = cursor.fetchall()

    for book in borrowed_books:
        books_listbox.insert(tk.END, book[0])

    # Close the cursor but keep the connection open for later
    cursor.close()

    def return_selected():
        connection = connect_to_db()
        cursor = connection.cursor()

        selected_index = books_listbox.curselection()

        if selected_index:
            selected_book = books_listbox.get(selected_index)

            # Get book and user IDs
            cursor.execute("SELECT id FROM books WHERE title = %s", (selected_book,))
            book_id = cursor.fetchone()[0]
            cursor.execute("SELECT id FROM users WHERE username = %s", (current_user,))
            user_id = cursor.fetchone()[0]

            # Check if the book is borrowed by the user
            cursor.execute("SELECT due_date FROM books WHERE id = %s AND borrowed_by = %s", (book_id, user_id))
            book_info = cursor.fetchone()

            if book_info:
                due_date = book_info[0]
                return_date = datetime.now().date()

                # Calculate penalty if the book is overdue
                days_overdue = (return_date - due_date).days if due_date and return_date > due_date else 0
                penalty = days_overdue * 25 if days_overdue > 0 else 0

                # Record the return in return_books table
                cursor.execute("INSERT INTO return_books (book_id, user_id, return_date, penalty) "
                               "VALUES (%s, %s, %s, %s)", (book_id, user_id, return_date, penalty))

                # Update the books table to mark the book as returned
                cursor.execute("UPDATE books SET borrowed_by = NULL, due_date = NULL WHERE id = %s", (book_id,))
                connection.commit()

                messagebox.showinfo("Success", f"You have returned '{selected_book}'. Penalty: {penalty} pesos.")
            else:
                messagebox.showerror("Error", "You haven't borrowed this book.")

        connection.close()
        return_books()  # Refresh the view

    # Bottom frame for Return and Back buttons
    bot_frame = tk.Frame(root, bg='white')
    bot_frame.pack(side="bottom", pady=20)  # Positioned at the bottom with padding

    return_button = tk.Button(bot_frame, text="Return", command=return_selected, font=("Arial", 30))
    return_button.pack(pady=10)  # Centered return button with padding

    back_button = tk.Button(bot_frame, text="Back", command=open_main_menu, font=("Arial", 30))
    back_button.pack(pady=10)  # Centered back button with padding

    # Close connection after the UI setup is complete and after the return operation
    connection.close()


def add_books():
    clear_window()
    root.config(bg="white")  # Set main window background color

    # Header section (Title)
    header_frame = tk.Frame(root, bg="#333333", height=80)
    header_frame.pack(fill="x", side="top")

    title_label = tk.Label(header_frame, text=f"Add New Books", fg="white", bg="#333333",
                           font=("Arial", 40, "bold"))
    title_label.pack(pady=20)

    # Left-side buttons in a vertical frame
    button_frame = tk.Frame(root, bg="#D3D3D3", width=300)
    button_frame.pack(side="left", fill="y", padx=10, pady=20)

    # Buttons for library functionalities
    view_books_button = tk.Button(button_frame, text="📚 View Books", width=20, command=view_books, font=("Arial", 18),
                                  anchor="w", bg="#E0E0E0")
    view_books_button.pack(pady=10, padx=10, fill="x")

    borrow_books_button = tk.Button(button_frame, text="📥 Borrow Books", width=20, command=borrow_books,
                                    font=("Arial", 18), anchor="w", bg="#E0E0E0")
    borrow_books_button.pack(pady=10, padx=10, fill="x")

    return_books_button = tk.Button(button_frame, text="📤 Return Books", width=20, command=return_books,
                                    font=("Arial", 18), anchor="w", bg="#E0E0E0")
    return_books_button.pack(pady=10, padx=10, fill="x")

    add_books_button = tk.Button(button_frame, text="📖 Add Books", width=20, command=add_books, font=("Arial", 18),
                                 anchor="w", bg="#E0E0E0")
    add_books_button.pack(pady=10, padx=10, fill="x")

    log_out_button = tk.Button(button_frame, text="🔒 Logout", width=20, command=show_login, font=("Arial", 18),
                               anchor="w", bg="#E0E0E0")
    log_out_button.pack(pady=10, padx=10, fill="x")

    # Book title input
    book_title_label = tk.Label(root, text="Book Title:", bg='white', font=("Arial", 30))
    book_title_label.place(x=350, y=150)  # Position with x, y coordinates

    book_title_entry = tk.Entry(root, width=20, font=("Arial", 40))
    book_title_entry.place(x=350, y=200)  # Position with x, y coordinates

    def add_new_book():
        connection = connect_to_db()
        cursor = connection.cursor()

        new_title = book_title_entry.get()

        if new_title:
            cursor.execute("INSERT INTO books (title) VALUES (%s)", (new_title,))
            connection.commit()
            messagebox.showinfo("Success", f"Book '{new_title}' added successfully!")
            book_title_entry.delete(0, tk.END)  # Clear entry field after adding
        else:
            messagebox.showwarning("Input Error", "Please enter a book title.")

        connection.close()
        display_books()  # Refresh the book list display

    # Bottom frame for Add and Back buttons
    bot_frame = tk.Frame(root, bg='white')
    bot_frame.pack(side="bottom", pady=20)  # Positioned at the bottom with padding

    add_button = tk.Button(bot_frame, text="Add Book", command=add_new_book, font=("Arial", 30))
    add_button.pack(pady=10)  # Centered add button with padding

    back_button = tk.Button(bot_frame, text="Back", command=open_main_menu, font=("Arial", 30))
    back_button.pack(pady=10)  # Centered back button with padding

    # Display the current book list
    book_list_label = tk.Label(root, text="Current Book List:", bg='white', font=("Arial", 30))
    book_list_label.place(x=350, y=290)  # Position with x, y coordinates

    books_list = tk.Text(root, bg='lightyellow', width=50, height=10, font=("Arial", 20))
    books_list.place(x=350, y=350)  # Position with x, y coordinates

    # Function to fetch and display the books
    def display_books():
        books_list.config(state=tk.NORMAL)  # Enable editing to insert text
        books_list.delete(1.0, tk.END)  # Clear previous content

        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT title, borrowed_by FROM books")
        book_list = cursor.fetchall()

        for book in book_list:
            title, borrowed_by = book
            status = "Available" if not borrowed_by else "Borrowed"
            books_list.insert(tk.END, f"{title} - {status}\n")

        books_list.config(state=tk.DISABLED)  # Disable editing

        connection.close()

    display_books()  # Initially display the books

show_login()
root.mainloop()


