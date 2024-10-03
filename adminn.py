from connect import connect
import mysql.connector as sq

cursor, con = connect()  # Establish connection


# Create all the necessary tables
def create_tables(cursor, con):
    try:
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS admin (
                            admin_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                            admin_name VARCHAR(100) NOT NULL,
                            user_name VARCHAR(100) NOT NULL,
                            password VARCHAR(100) NOT NULL,
                            phone_number VARCHAR(10) NOT NULL,
                            mail_id VARCHAR(50) NOT NULL
                        )
                        ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS bus (
                    bus_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    bus_name VARCHAR(100),
                    bus_type ENUM ('AC-Sleeper', 'Non-AC-Sleeper', 'AC-Seater', 'Non-AC-Seater'),
                    departure_time TIME NOT NULL,
                    arrival_time TIME NOT NULL,
                    source VARCHAR(100) NOT NULL,
                    destination VARCHAR(100) NOT NULL,
                    seats_available INTEGER NOT NULL,
                    fare DECIMAL(10,2)
                )
                ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    customer_name VARCHAR(100) NOT NULL,
                    user_name VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(10) NOT NULL,
                    mail_id VARCHAR(50) NOT NULL
                )
                ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Booking (
                    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    booking_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    bus_id INTEGER NOT NULL,
                    customer_name VARCHAR(100) NOT NULL,
                    FOREIGN KEY (bus_id) REFERENCES bus(bus_id)
                )
                ''')

        print("All tables created successfully.")
        con.commit()  # Commit all changes to the database
    except sq.Error as e:
        print(f"Error creating tables: {e}")


def insert_bus_1(cursor, con):
    try:
        cursor.execute("""INSERT INTO bus (bus_name, bus_type, departure_time, arrival_time, source, destination, seats_available, fare)
                       VALUES ('Rajaganapathy', 'Non-AC-Seater', '08:00', '05:00', 'Pondy', 'Tindivanam', 50, 25.00)""")
        cursor.execute("""INSERT INTO bus(bus_name, bus_type, departure_time, arrival_time, source, destination, seats_available, fare)
                       VALUES('Thamarai', 'AC-Seater', '07:00', '03:00', 'Villupuram', 'Pondy', 45, 22.50)""")
        cursor.execute("""INSERT INTO bus(bus_name, bus_type, departure_time, arrival_time, source, destination, seats_available, fare)
                       VALUES('PRTC', 'Non-AC-Sleeper', '05:00', '10:00', 'Pondy', 'Karaikal', 30, 110.00)""")
        cursor.execute("""INSERT INTO bus(bus_name, bus_type, departure_time, arrival_time, source, destination, seats_available, fare)
                       VALUES('Town bus', 'AC-Sleeper', '06:00', '12:00', 'Pondy', 'Bangalore', 45, 122.00)""")
        con.commit()
        print(" Bus data inserted successfully.")

    except sq.Error as e:
        print(f"Error inserting data: {e}")


def update_fare(cursor, con):
    try:
        cursor.execute("UPDATE bus SET fare = 700 WHERE bus_type = %s", ('AC-Sleeper',))
        cursor.execute("UPDATE bus SET fare = 550 WHERE bus_type = %s", ('AC-Seater',))
        cursor.execute("UPDATE bus SET fare = 600 WHERE bus_type = %s", ('Non-AC-Sleeper',))
        cursor.execute("UPDATE bus SET fare = 450 WHERE bus_type = %s", ('Non-AC-Seater',))

        con.commit()
        print("Fare values updated successfully.")

    except Exception as e:
        print(f"Error updating fare values: {e}")

def insert_bus(bname, btype, dt, at, source, destination, seats, fare):
    try:

        cursor.execute(
            "INSERT INTO bus (bus_name, bus_type, departure_time, arrival_time, source, destination, seats_available, fare) "
            "VALUES (%s%s%s%s%s%s%s%s)", (bname, btype, dt, at, source, destination, seats, fare))
        con.commit()
        print(" Customer data inserted successfully.")

    except sq.Error as e:
        print(f"Error inserting data: {e}")


def insert_admin(name, username, password, ph, mail):
    try:

        cursor.execute(
            "INSERT INTO admin (admin_name, user_name, password, phone_number, mail_id) "
            "VALUES (%s,%s,%s,%s,%s)", (name, username, password, ph, mail))
        con.commit()
        print(" Admin data inserted successfully.")

    except sq.Error as e:
        print(f"Error inserting data: {e}")


def insert_customer(name, username, password, ph, mail, gender):
    try:

        cursor.execute("INSERT INTO customers (customer_name, user_name, password, phone_number, mail_id, gender) VALUES (%s,"
                       "%s,%s,%s,%s,%s)", (name, username, password, ph, mail, gender))
        con.commit()
        print(" Customer data inserted successfully.")

    except sq.Error as e:
        print(f"Error inserting data: {e}")


# Function to display available buses
def show_available_buses(cursor):
    cursor.execute("SELECT * FROM bus WHERE seats_available > 0")
    buses = cursor.fetchall()
    if buses:
        print("Available Buses:")
        for bus in buses:
            print(
                f"Bus ID: {bus[0]}, Bus name: {bus[1]}, Bus type: {bus[2]}, Seats Available: {bus[7]}, fare: {bus[8]}")
    else:
        print("No buses available!")


def show_customers(username, password):
    try:
        cursor.execute("SELECT * FROM customers WHERE user_name = %s AND password = %s", (username, password))
        customers = cursor.fetchall()
        if customers:
            print("Customer details:")
            # print(f"Full customer record: {customers}")
            for customer in customers:
                print(
                    f"Customer ID: {customer[0]}, Customer name: {customer[1]}, phone number: {customer[4]}, mail ID: {customer[5]}")
            return True
        else:
            print("Username or password incorrect!")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")


def show_admin(username, password):
    try:
        cursor.execute("SELECT * FROM admin WHERE user_name = %s AND password = %s", (username, password))
        admins = cursor.fetchall()
        if admins:
            print("Admin details:")
            # print(f"Full customer record: {customers}")
            for admin in admins:
                print(
                    f"Admin ID: {admin[0]}, Admin name: {admin[1]}, phone number: {admin[4]}, mail ID: {admin[5]}")
            return True
        else:
            print("Username or password incorrect!")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")


def book_bus_ticket():
    try:
        customer_name = input("Enter customer name: ")
        # print("Available buses:")
        # show_available_buses(cursor)

        bus_id = input("Enter the bus ID you want to book: ")
        cursor.execute("SELECT seats_available, fare FROM bus WHERE bus_id = %s", (bus_id,))
        bus = cursor.fetchone()

        if bus is None:
            print("Invalid bus ID. Please try again.")
            return

        seats_available = bus[0]
        fare_per_seat = bus[1]
        print(f"Seats available: {seats_available}")
        print(f"Fare per seat: {fare_per_seat}")

        seats_to_book = int(input("Enter the number of seats to book: "))

        if seats_to_book > seats_available:
            print(f"Not enough seats available. Only {seats_available} seats left.")
            return

        total_fare = seats_to_book * fare_per_seat
        print(f"Total fare for {seats_to_book} seat(s): {total_fare}")

        confirm = input(f"Do you want to proceed with the booking for {total_fare}? (yes/no): ").lower()

        if confirm != 'yes':
            print("Booking cancelled.")
            return

        new_seats_available = seats_available - seats_to_book
        cursor.execute("UPDATE bus SET seats_available = %s WHERE bus_id = %s", (new_seats_available, bus_id))
        con.commit()

        cursor.execute("""
            INSERT INTO booking (customer_name, bus_id, no_of_seats, total_fare)
            VALUES (%s, %s, %s, %s)
        """, (customer_name, bus_id, seats_to_book, total_fare))
        con.commit()

        print(f"Booking successful! You have booked {seats_to_book} seat(s) for a total fare of {total_fare}.")

    except Exception as e:
        con.rollback()
        print(f"An error occurred during booking: {e}")


# def book_bus_ticket1():
#     try:
#             customer_name = input("Enter customer name: ")
#             bus_id = int(input("Enter the Bus ID you want to book a ticket for: "))
#             cursor.execute("SELECT bus_id, bus_name, source, destination, seats_available, fare"
#                            " FROM bus WHERE seats_available > 0 and bus_id = %s", (bus_id, ))
#             buses = cursor.fetchall()
#             if buses:
#                 print("Fare details of selected bus:")
#                 for bus in buses:
#                     print(f"Bus ID: {bus[0]},Bus name: {bus[1]}, Source: {bus[2]}, Destination: {bus[3]}, Available Seats: {bus[4]}, "
#                           f"Fare: ${bus[5]}")
#
#                     confirm = input("Do you want to book this bus ticket? (yes/no): ").lower()
#
#                     if confirm == "yes":
#
#                         cursor.execute("UPDATE bus SET seats_available = seats_available - 1 WHERE bus_id = %s",
#                                        (bus_id,))
#
#                         cursor.execute("INSERT INTO booking (bus_id, customer_name) VALUES (%s, %s)",
#                                        (bus_id, customer_name))
#                         con.commit()
#                         print("Bus ticket successfully booked!")
#                     else:
#                         print("Booking cancelled.")
#
#             else:
#                 print("No buses with available seats found.")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")


# Function to view all bookings
def view_bookings(cursor):
    cursor.execute("SELECT * FROM Booking")
    bookings = cursor.fetchall()
    if bookings:
        print("All Bookings:")
        for booking in bookings:
            print(f"DateTime: {booking[0]}, Booking ID: {booking[1]}, Bus ID: {booking[2]}, Customer: {booking[3]}, no_of_seats: {booking[4]}, total_fare: {booking[5]}")
    else:
        print("No bookings yet!")


def view_my_bookings(name, cursor):

    cursor.execute("SELECT * FROM Booking WHERE customer_name = %s",(name,))
    bookings = cursor.fetchall()
    if bookings:
        print(" Your Bookings:")
        for booking in bookings:
            print(f"DateTime: {booking[0]}, Booking ID: {booking[1]}, Bus ID: {booking[2]}, Customer: {booking[3]}, no_of_seats: {booking[4]}, total_fare: {booking[5]}")
    else:
        print("No bookings yet!")

def view_admins(cursor):
    cursor.execute("SELECT * FROM admin")
    admins = cursor.fetchall()
    if admins:
        print("All admins:")
        for admin in admins:
            print(
                f"Admin ID: {admin[0]}, Admin name: {admin[1]}, phone number: {admin[4]}, mail ID: {admin[5]}")
    else:
        print("No admins yet!")

def view_buses(cursor):
    cursor.execute("SELECT * FROM bus")
    buses = cursor.fetchall()
    if buses:
        print("All Buses:")
        for bus in buses:
            print(
                f"Bus ID: {bus[0]}, Bus name: {bus[1]}, Bus type: {bus[2]}, departure time: {bus[3]}, arrival time: {bus[4]}, "
                f"Source: {bus[5]} destination: {bus[6]}, Seats available : {bus[7]}, Fare : {bus[8]}")
    else:
        print("No buses registered!")


def view_customers(cursor):
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    if customers:
        print("All Customer details:")
        for customer in customers:
            print(
                f"Customer ID: {customer[0]}, Customer name: {customer[1]}, Phone number: {customer[4]}, Mail ID: {customer[5]}")
    else:
        print("No customers found.")


def update_booking():
    try:
        cursor.execute("ALTER TABLE booking ADD COLUMN no_of_seats INT")
        con.commit()
        print("Column 'no_of_seats' added to 'booking' table successfully.")

    except sq.Error as e:
        print(f"Error altering table: {e}")


def update_booking1(cursor):
    try:
        cursor.execute("ALTER TABLE booking ADD COLUMN total_fare FLOAT")
        con.commit()
        print("Column 'total_fare' added to 'booking' table successfully.")

    except sq.Error as e:
        print(f"Error altering table: {e}")

def update_customers(cursor):
    try:
        cursor.execute("ALTER TABLE customers ADD COLUMN gender ENUM ('Male','Female')")
        con.commit()
        print("Column 'gender' added to 'customers' table successfully.")

    except sq.Error as e:
        print(f"Error altering table: {e}")


def update_bus(bus_name):
    try:
        cursor.execute("UPDATE Bus SET seats_available = seats_available + 1 WHERE bus_name = %s", (bus_name,))
        con.commit()
        print(f"1 seat is added to the {bus_name} bus.")

    except sq.Error as e:
        print(f"Error updating bus table: {e}")


def filter_buses1(cursor):
    print("Bus Filtering Options:")

    ac_preference = input("Filter by Bus Type (AC, Non-AC, Both): ").lower()
    seat_preference = input("Filter by Seat Type (Seater, Sleeper, Both): ").lower()

    query = """
        SELECT bus_name, bus_type, seat_type, seats_available, source, destination, fare
        FROM Bus
        WHERE seats_available > 0
    """

    conditions = []

    if ac_preference in ['ac', 'non-ac']:
        conditions.append(f"bus_type = '{ac_preference}'")

    if seat_preference in ['seater', 'sleeper']:
        conditions.append(f"seat_type = '{seat_preference}'")

    if conditions:
        query += " AND " + " AND ".join(conditions)

    query += " ORDER BY seats_available DESC, bus_type , seat_type "

    cursor.execute(query)
    buses = cursor.fetchall()

    if buses:
        print("\nAvailable Buses:")
        for bus in buses:
            print(f"Bus Name: {bus[0]}, Type: {bus[1]}, Seat Type: {bus[2]}, Available Seats: {bus[3]}, "
                  f"Source: {bus[4]}, Destination: {bus[5]}, Fare: {bus[6]}")
    else:
        print("No buses match your filters or have available seats.")


def filter_buses(cursor):
    print("Bus Filtering Options:")

    preference = input("Filter by Bus Type (AC-sleeper, AC-Seater, Non-AC-Sleeper, Non-AC-Seater, All): ").lower()

    query = """
        SELECT bus_name, bus_type, seats_available, source, destination, fare
        FROM Bus
        WHERE seats_available > 0
    """

    conditions = []

    if preference in ['ac-seater', 'non-ac-seater', 'ac-sleeper', 'non-ac-sleeper']:
        conditions.append(f"bus_type = '{preference}'")

    if conditions:
        query += " AND " + " AND ".join(conditions)

    query += " ORDER BY seats_available DESC"

    cursor.execute(query)
    buses = cursor.fetchall()

    if buses:
        print("\nAvailable Buses:")
        for bus in buses:
            print(f"Bus Name: {bus[0]}, Type: {bus[1]}, Available Seats: {bus[2]}, "
                  f"Source: {bus[3]}, Destination: {bus[4]}, Fare: {bus[5]}")
    else:
        print("No buses match your filters or have available seats.")


def filter_buses_(cursor):
    print("Please enter your travel details:")

    source = input("Enter source location: ")
    destination = input("Enter destination location: ")

    query = """
        SELECT bus_id, bus_name, bus_type, seats_available, fare
        FROM Bus
        WHERE seats_available > 0
          AND source = %s
          AND destination = %s
        ORDER BY seats_available DESC
    """

    cursor.execute(query, (source, destination))
    buses = cursor.fetchall()

    if buses:
        print("\nAvailable Buses:")
        for bus in buses:
            print(f"Bus_id : {bus[0]}, Bus_name : {bus[1]}, Bus_type: {bus[2]}, Seats available: {bus[3]}, Fare: {bus[4]}")
    else:
        print("No buses available for the given  source and destination.")


def cancel_ticket(booking_id, cursor, con):
    try:
        cursor.execute("""
            SELECT b.bus_type, bk.no_of_seats, bk.total_fare, bk.bus_id 
            FROM booking bk
            JOIN bus b ON bk.bus_id = b.bus_id
            WHERE bk.booking_id = %s
        """, (booking_id,))
        booking = cursor.fetchone()

        if booking is None:
            print("Invalid booking ID.")
            return

        bus_type, no_of_seats, total_fare, bus_id = booking
        print(f"Your current booking has {no_of_seats} seat(s).")

        cancel_type = input("Do you want to cancel all seats or specific seats? (all/specific): ").lower()

        if cancel_type == "specific":
            seats_to_cancel = int(input("How many seats would you like to cancel?: "))
            if seats_to_cancel > no_of_seats:
                print(f"You only have {no_of_seats} seat(s) booked.")
                return
        else:
            seats_to_cancel = no_of_seats

        if "AC" in bus_type:
            cancellation_fee_percentage = 0.50
        else:
            cancellation_fee_percentage = 0.25

        total_seat_fare = total_fare / no_of_seats
        refund_amount = seats_to_cancel * total_seat_fare * (1 - cancellation_fee_percentage)

        print(f"You will be refunded {refund_amount} for {seats_to_cancel} seat(s) after a {cancellation_fee_percentage*100}% cancellation fee.")

        confirm = input(f"Do you want to proceed with cancellation and refund of {refund_amount}? (yes/no): ").lower()

        if confirm != 'yes':
            print("Cancellation aborted.")
            return

        cursor.execute("SELECT seats_available FROM bus WHERE bus_id = %s", (bus_id,))
        seats_available = cursor.fetchone()[0]
        new_seats_available = seats_available + seats_to_cancel
        cursor.execute("UPDATE bus SET seats_available = %s WHERE bus_id = %s", (new_seats_available, bus_id))

        if seats_to_cancel == no_of_seats:
            cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
        else:
            new_seats_booked = no_of_seats - seats_to_cancel
            new_total_fare = new_seats_booked * total_seat_fare
            cursor.execute("""
                UPDATE booking 
                SET no_of_seats = %s, total_fare = %s 
                WHERE booking_id = %s
            """, (new_seats_booked, new_total_fare, booking_id))

        con.commit()
        print(f"Successfully canceled {seats_to_cancel} seat(s). Refund of {refund_amount} processed.")

    except Exception as e:
        con.rollback()
        print(f"An error occurred during cancellation: {e}")


def delete_bus(bus_name):
    try:
        if not bus_name:
            print(f"Bus with name '{bus_name}' does not exist .")
            return

        cursor.execute("DELETE FROM bus WHERE bus_name = %s", (bus_name,))
        if cursor.rowcount == 0:
            print(f"No bus found with the name '{bus_name}'.")
        else:
            con.commit()
            print(f"Bus with name '{bus_name}' has been deleted successfully.")
    except sq.Error :
        con.rollback()
        print(f"Error deleting the bus: This book already have booking.")


# Main function to run everything
def main(cursor, con):
    if cursor and con:
        # create_tables(cursor, con)  # Create the necessary tables
        view_buses(cursor)
        # update_fare(cursor, con)
        # show_customers(username='sheethal',password='sheethal')
        # insert_admin(name='bharathi',username='bharathi', password='bharathi', ph='9876543210', mail='bharathi@gmail'
        #                                                                                             '.com')
        # update_customers(cursor)
        # update_booking1(cursor)

    else:
        print("Connection to the database failed.")


if __name__ == "__main__":
    main(cursor, con)
