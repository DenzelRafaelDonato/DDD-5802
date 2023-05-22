import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from PIL import Image, ImageTk

import mysql.connector
from mysql.connector import Error


class CinemaBookingSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Cinema Ticket Booking")
        self.master.geometry("800x600")

        self.style = ttk.Style()
        self.style.configure("TButton", background="#FFFFFF")
        self.style.configure("TButton.selected", background="#FFFFFF")
        self.style.configure("TLabel", font=("Times New Roman", 12))
        self.style.configure("TCombobox", background="white")

        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Load and resize the background image
        background_image = Image.open("test.png")
        width = 960
        height = 600

        # Resize the image using LANCZOS resampling
        resized_image = background_image.resize((width, height))

        # Save the resized image
        resized_image.save("test.png")

        self.background_photo = ImageTk.PhotoImage(resized_image)
        self.background_label = Label(self.main_frame, image=self.background_photo)
        self.background_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.name_label = ttk.Label(self.main_frame, text="Name:")
        self.name_label.grid(row=0, column=0,  padx=5, pady=10)

        self.first_name_entry = ttk.Entry(self.main_frame, width=20)
        self.first_name_entry.grid(row=0, column=1, pady=5)

        self.middle_initial_entry = ttk.Entry(self.main_frame, width=5)
        self.middle_initial_entry.grid(row=0, column=2, padx=5, pady=5)

        self.last_name_entry = ttk.Entry(self.main_frame, width=20)
        self.last_name_entry.grid(row=0, column=3, pady=5)

        self.movie_label = ttk.Label(self.main_frame, text="Movie:")
        self.movie_label.grid(row=1, column=0, padx=5, pady=10)

        self.movie_choice = StringVar()
        self.movie_choice.set("Select a movie")

        self.movie_option_menu = ttk.OptionMenu(self.main_frame, self.movie_choice, "Select a movie", "Titanic",
                                                "Beauty and the Beast", "Avengers: Endgame", command=self.update_seats)
        self.movie_option_menu.grid(row=1, column=1, columnspan=3, padx=5, pady=10)

        self.time_label = ttk.Label(self.main_frame, text="Time:")
        self.time_label.grid(row=2, column=0, padx=5, pady=10)

        self.time_choice = StringVar()
        self.time_choice.set("Select a time")

        self.time_option_menu = ttk.OptionMenu(self.main_frame, self.time_choice, "Select a time", "10:30am-1:00pm",
                                               "1:20pm-4:00pm", "4:25pm-7:25pm", "7:30pm-10:30pm",
                                               command=self.update_seats)
        self.time_option_menu.grid(row=2, column=1, columnspan=3, padx=5, pady=10)

        self.location_label = ttk.Label(self.main_frame, text="Location:")
        self.location_label.grid(row=3, column=0, padx=5, pady=10)

        self.location_choice = StringVar()
        self.location_choice.set("Select a location")

        self.location_option_menu = ttk.OptionMenu(self.main_frame, self.location_choice, "Select a location",
                                                   "Manila Branch", "Sta. Mesa Branch", "Caloocan Branch",
                                                   command=self.update_seats)
        self.location_option_menu.grid(row=3, column=1, columnspan=3, padx=5, pady=10)

        self.ticket_type_label = ttk.Label(self.main_frame, text="Ticket: ")
        self.ticket_type_label.grid(row=4, column=0, padx=5, pady=10)
        self.ticket_type_choice = StringVar()
        self.ticket_type_choice.set("Select a Ticket Type")
        self.ticket_type_option_menu = ttk.OptionMenu(self.main_frame, self.ticket_type_choice, "Select a Ticket Type",
                                                      "Normal",
                                                      "Date-Friendly", "Family", "VIP",
                                                      command=self.update_seats)
        self.ticket_type_option_menu.grid(row=4, column=1, columnspan=3, padx=5, pady=10)

        self.seat_buttons = []
        self.selected_seats = []

        rows = 5
        cols = 10

        self.total_cost_label = ttk.Label(self.main_frame, text="Total Cost: P0")
        self.total_cost_label.grid(row=rows + 6, column=0, columnspan=cols, padx=5, pady=10)

        self.book_button = ttk.Button(self.main_frame, text="Book", command=self.confirm_booking, state=DISABLED)
        self.book_button.grid(row=rows + 7, column=0, columnspan=cols, padx=5, pady=10)

        self.display_button = ttk.Button(self.main_frame, text="Display Customers", command=self.display_customers)
        self.display_button.grid(row=rows + 8, column=0, columnspan=cols, padx=5, pady=10)

        self.delete_button = ttk.Button(self.main_frame, text="Delete Customers", command=self.delete_customers)
        self.delete_button.grid(row=rows + 9, column=0, columnspan=cols, padx=5, pady=10)

        self.ticket_prices = {
            "Normal": 250,
            "Date-Friendly": 300,
            "Family": 350,
            "VIP": 400
        }
        self.booking_code = None

        # Admin password
        self.admin_password = "denzelpogi69"

    def update_seats(self, event):
        selected_movie = self.movie_choice.get()
        selected_time = self.time_choice.get()
        selected_location = self.location_choice.get()

        if selected_movie != "Select a movie" and selected_time != "Select a time" and selected_location != "Select a location":
            self.book_button.config(state=NORMAL)
            self.reset_seats()
            self.create_seat_buttons()  # Call the function to create seat buttons based on the selected ticket type
        else:
            self.book_button.config(state=DISABLED)
            self.reset_seats()

    def create_seat_buttons(self):
        selected_ticket_type = self.ticket_type_choice.get()
        cols = 10

        for seat_button in self.seat_buttons:
            seat_button.destroy()  # Destroy the existing seat buttons

        self.seat_buttons = []  # Reset the list of seat buttons

        if selected_ticket_type == "Normal":
            row = 1
            for row in range(1):
                for col in range(cols):
                    seat_button = ttk.Button(self.main_frame, text=f"Row {1}, Seat {col + 1}",
                                             command=lambda r=row, c=col: self.select_seat(r, c))
                    seat_button.grid(row=row + 5, column=col, padx=5, pady=5)
                    self.seat_buttons.append(seat_button)

            self.update_total_cost()


        elif selected_ticket_type == "Date-Friendly":
            row = 1
            for i in range(2):
                current_row = row + i
                for col in range(cols):
                    seat_button = ttk.Button(self.main_frame, text=f"Row {current_row + 1}, Seat {col + 1}",
                                             command=lambda r=current_row, c=col: self.select_seat(r, c))
                    seat_button.grid(row=current_row + 5, column=col, padx=5, pady=5)
                    self.seat_buttons.append(seat_button)

            self.update_total_cost()

        elif selected_ticket_type == "Family":
            row = 1
            for row in range(1):
                for col in range(cols):
                    seat_button = ttk.Button(self.main_frame, text=f"Row {4}, Seat {col + 1}",
                                             command=lambda r=row, c=col: self.select_seat(r, c))
                    seat_button.grid(row=row + 5, column=col, padx=5, pady=5)
                    self.seat_buttons.append(seat_button)

            self.update_total_cost()


        elif selected_ticket_type == "VIP":
            row = 1
            for row in range(1):
                for col in range(cols):
                    seat_button = ttk.Button(self.main_frame, text=f"Row {5}, Seat {col + 1}",
                                             command=lambda r=row, c=col: self.select_seat(r, c))
                    seat_button.grid(row=row + 5, column=col, padx=5, pady=5)
                    self.seat_buttons.append(seat_button)

            self.update_total_cost()

    def select_seat(self, row, col):
        seat = (row, col)
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
        else:
            self.selected_seats.append(seat)
        self.update_total_cost()

    def reset_seats(self):
        self.selected_seats = []
        for seat_button in self.seat_buttons:
            seat_button.config(state=NORMAL, style="TButton")

        self.update_total_cost()

    def update_total_cost(self):
        selected_ticket_type = self.ticket_type_choice.get()
        ticket_price = self.ticket_prices.get(selected_ticket_type, 0)
        total_cost = ticket_price * len(self.selected_seats)
        self.total_cost_label.config(text=f"Total Cost: P{total_cost}")

    def generate_booking_code(self):
        characters = string.ascii_uppercase + string.digits
        self.booking_code = ''.join(random.choice(characters) for _ in range(6))
        return self.booking_code

    def generate_receipt_code(self):
        characters = string.digits
        self.receipt_code = ''.join(random.choice(characters) for _ in range(18))
        return self.receipt_code

    def reset_choices(self):
        self.movie_choice.set("Select a movie")
        self.time_choice.set("Select a time")
        self.location_choice.set("Select a location")
        self.ticket_type_choice.set("Normal")
        self.reset_seats()

    def confirm_booking(self):
        confirm = messagebox.askyesno("Confirm Booking", "Are you sure you want to proceed with the booking?")
        if confirm:
            first_name = self.first_name_entry.get()
            middle_initial = self.middle_initial_entry.get()
            last_name = self.last_name_entry.get()
            if first_name and middle_initial and last_name and self.selected_seats:
                customersName = f"{first_name} {middle_initial} {last_name}"
                customersID = self.generate_booking_code()
                location = self.location_choice.get()
                movieP = self.movie_choice.get()
                timeP = self.time_choice.get()
                tickets = len(self.selected_seats)
                ticket_type = self.ticket_type_choice.get()
                seatP = ', '.join([f"Row {row + 1}, Seat {col + 1}" for row, col in self.selected_seats])
                receipt = self.generate_receipt_code()

                messagebox.showinfo(
                    "Booking Successful",
                    f"You have booked {tickets} seat(s) for {movieP}\n"
                    f"Time: {timeP}\n"
                    f"Location: {location}\n"
                    f"Ticket Type: {ticket_type}\n"
                    f"Total Cost: {self.total_cost_label.cget('text')[12:]}\n\n"
                    f"Name: {customersName}\n"
                    f"Booking Code: {receipt}"
                )
                customersName = f"{first_name} {middle_initial} {last_name}"
                customersID = self.generate_booking_code()
                location = self.location_choice.get()
                movieP = self.movie_choice.get()
                timeP = self.time_choice.get()
                tickets = len(self.selected_seats)
                cinema = self.ticket_type_choice.get()
                priceP = self.total_cost_label.cget('text')[12:]
                seatP = ', '.join([f"Row {row + 1} Seat {col + 1}" for row, col in self.selected_seats])
                try:
                    connect = mysql.connector.connect(
                        host="localhost",
                        database="movie_customers_database",
                        user="root",
                        password="Donato09!"
                    )
                    query = "INSERT INTO customers_table (CustomersID, CustomersName, LocationBranch, Movie, Cinema, TimeBought, Tickets, Price, SeatPosition) " \
                            "VALUES ('" + customersID + "', '" + customersName + "', '" + location + "', '" + movieP + "', '" + cinema + "', '" + timeP + "', '" + str(
                        tickets) + "','" + priceP + "','" + seatP + "')"
                    cur = connect.cursor()
                    cur.execute(query)
                    connect.commit()
                    cur.close()
                except Error as error:
                    print("\nInsert Data: Failed {}".format(error))
                finally:
                    if connect.is_connected():
                        connect.close()
                        print("\nMySQL Connection Status: CLOSED")

                self.reset_choices()
                self.first_name_entry.delete(0, END)
                self.middle_initial_entry.delete(0, END)
                self.last_name_entry.delete(0, END)
            else:
                messagebox.showwarning("Incomplete Information", "Please select at least one seat and enter your name.")
        else:
            self.reset_choices()
            self.first_name_entry.delete(0, END)
            self.middle_initial_entry.delete(0, END)
            self.last_name_entry.delete(0, END)

    def display_customers(self):
        password = simpledialog.askstring("Admin Password", "Enter Admin Password:", show="*")
        if password == "denzelpogi69":
            try:
                connect = mysql.connector.connect(
                    host="localhost",
                    database="movie_customers_database",
                    user="root",
                    password="Donato09!"
                )
                query = "SELECT CustomersID, CustomersName, LocationBranch, Movie, Cinema, TimeBought, Tickets, Price, SeatPosition FROM customers_table"
                cur = connect.cursor()
                cur.execute(query)
                rows = cur.fetchall()

                # Create a new window for displaying customers
                customers_window = Toplevel()
                customers_window.title("Customer List")

                # Create a treeview widget to display the customer data
                tree = ttk.Treeview(customers_window)

                # Define columns
                tree["columns"] = (
                    "Customer ID", "Customer Name", "Location", "Movie", "Cinema", "Time", "Tickets", "Price",
                    "SeatPosition")

                # Format columns
                tree.column("#0", width=0, stretch=NO)
                tree.column("Customer ID", anchor=CENTER, width=100)
                tree.column("Customer Name", anchor=CENTER, width=100)
                tree.column("Location", anchor=CENTER, width=100)
                tree.column("Movie", anchor=CENTER, width=110)
                tree.column("Cinema", anchor=CENTER, width=100)
                tree.column("Time", anchor=CENTER, width=100)
                tree.column("Tickets", anchor=CENTER, width=80)
                tree.column("Price", anchor=CENTER, width=80)
                tree.column("SeatPosition", anchor=CENTER, width=200)

                # Create headings
                tree.heading("#0", text="", anchor=CENTER)
                tree.heading("Customer ID", text="Customer ID", anchor=CENTER)
                tree.heading("Customer Name", text="Customer Name", anchor=CENTER)
                tree.heading("Location", text="Location", anchor=CENTER)
                tree.heading("Movie", text="Movie", anchor=CENTER)
                tree.heading("Cinema", text="Cinema", anchor=CENTER)
                tree.heading("Time", text="Time", anchor=CENTER)
                tree.heading("Tickets", text="Tickets", anchor=CENTER)
                tree.heading("Price", text="Price", anchor=CENTER)
                tree.heading("SeatPosition", text="SeatPosition", anchor=CENTER)

                # Insert data into the treeview
                for row in rows:
                    tree.insert("", "end", values=row)

                tree.pack(fill="both", expand=True)

                cur.close()
            except Error as error:
                print("\nDisplay Data: Failed {}".format(error))
            finally:
                if connect.is_connected():
                    connect.close()
                    print("\nMySQL Connection Status: CLOSED")
        else:
            messagebox.showerror("Access Denied", "Invalid Admin Password")

    def delete_customers(self):
        password = simpledialog.askstring("Admin Password", "Enter Admin Password:", show='*')
        if password == self.admin_password:
            customer_id = simpledialog.askstring("Delete Customers", "Enter Customer ID:")
            if customer_id:
                try:
                    connect = mysql.connector.connect(
                        host="localhost",
                        database="movie_customers_database",
                        user="root",
                        password="Donato09!"
                    )
                    query = "DELETE FROM customers_table WHERE CustomersID = '" + customer_id + "'"
                    cur = connect.cursor()
                    cur.execute(query)
                    connect.commit()

                    if cur.rowcount == 0:
                        messagebox.showerror("Delete Customer", "Customer ID not found.")
                    else:
                        messagebox.showinfo("Delete Customer", "Customer deleted successfully.")

                    cur.close()
                except Error as error:
                    print("\nDelete Data: Failed {}".format(error))
                finally:
                    if connect.is_connected():
                        connect.close()
                        print("\nMySQL Connection Status: CLOSED")
                    else:
                        messagebox.showwarning("Delete Customer", "Please enter a valid Customer ID.")
        else:
            messagebox.showwarning("Admin Password", "Incorrect admin password.")


root = Tk()
cinema_booking_system = CinemaBookingSystem(root)
root.mainloop()