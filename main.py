from connect import connect
from adminn import (insert_bus, insert_customer, show_available_buses, view_bookings,
                    show_customers, view_customers, view_buses, cancel_ticket, book_bus_ticket, insert_admin,
                    show_admin, view_admins, delete_bus, update_bus, view_my_bookings, filter_buses, filter_buses_)

if __name__ == "__main__":

    try:
        cursor, con = connect()  # Establish connection
        print("_________WELCOME TO BUS TICKET BOOKING SITE________")

        while True:
            op = input("1->Admin login\n"
                       "2->Customer login\n"
                       "3->Exit this window.\n"
                       "Enter the option: ")

            if op == '1':
                print("Welcome to admin page!\n")
                print("Enter Admin credentials.\n")
                username = input("Enter admin username: ")
                password = input("Enter password: ")
                while True:
                    if show_admin(username, password):
                        print("1->View all customers\n"
                              "2->Add bus\n"
                              "3->View buses\n"
                              "4->Update bus\n"
                              "5->Delete bus\n"
                              "6->Add new admin\n"
                              "7->View all admins\n"
                              "8->View all bookings\n"
                              "9->Logout\n")

                        o = input("Enter option: ")

                        if o == '1':
                            view_customers(cursor)
                        elif o == '2':
                            print("Enter bus details")
                            bname = input("Enter bus name: ")
                            print("Bus types can be AC-Sleeper/AC-Seater/Non-AC-Sleeper/Non-AC-Seater")
                            btype = input("Enter bus type: ")
                            dt = input("Enter departure time: ")
                            at = input("Enter arrival time: ")
                            source = input("Enter Starting point: ")
                            destination = input("Enter destination point: ")
                            seats = input("Enter seats available: ")
                            fare = input("Enter fare: ")
                            insert_bus(bname, btype, dt, at, source, destination, seats, fare)
                        elif o == '3':
                            view_buses(cursor)
                        elif o == '4':
                            bus_name = input("Enter bus name: ")
                            update_bus(bus_name)
                        elif o == '5':
                            view_buses(cursor)
                            bus_name = input("Enter bus name: ")
                            delete_bus(bus_name)
                        elif o == '6':
                            name = input("Enter your name: ")
                            username = input("Enter admin username: ")
                            password = input("Enter password: ")
                            ph = input("Enter phone number: ")
                            mail = input("Enter mail ID: ")
                            insert_admin(name, username, password, ph, mail)
                        elif o == '7':
                            view_admins(cursor)
                        elif o == '9':
                            print("Logging out from admin page.")
                            break
                        elif o == '8':
                            view_bookings(cursor)
                        else:
                            print("Invalid option. Please try again.")

            elif op == '2':

                print("Welcome to customer page.\n")
                print("1->New Registration\n"
                      "2->Sign in\n")
                opt = input("Enter option: ")

                while True:
                    if opt == '1':
                        print("New registration")
                        name = input("Enter your name: ")
                        username = input("Enter username: ")
                        password = input("Enter password: ")
                        ph = input("Enter your phone number: ")
                        mail = input("Enter mail ID: ")
                        gender = input("Enter gender: ")

                        insert_customer(name, username, password, ph, mail, gender)

                    elif opt == '2':
                        print("To check your details, please enter your username and password.\n")
                        username = input("Enter username: ")
                        password = input("Enter password: ")

                        while True:
                            if show_customers(username, password):

                                print("1->Book tickets\n"
                                      "2->Cancel tickets\n"
                                      "3->View my bookings\n"
                                      "4->Show available buses\n"
                                      "5->Logout\n")

                                option = input("Enter option: ")

                                if option == '1':
                                    print("Welcome to ticket booking site")

                                    print("1->Show all buses.\n"
                                          "2->filter buses based on bus type.\n"
                                          "3->filter buses based on source and destination\n")
                                    a = input("Enter option: ")
                                    if a == '1':
                                        show_available_buses(cursor)
                                        book_bus_ticket()
                                    elif a == '2':
                                        filter_buses(cursor)
                                        book_bus_ticket()
                                    elif a == '3':
                                        filter_buses_(cursor)
                                        book_bus_ticket()

                                elif option == '2':
                                    booking_id = input("Enter booking ID to cancel: ")
                                    cancel_ticket(booking_id, cursor, con)
                                elif option == '3':
                                    name = input("Enter your name :")
                                    view_my_bookings(name, cursor)
                                elif option == '4':
                                    show_available_buses(cursor)
                                elif option == '5':
                                    print("Logging out from customer page.")
                                    break

            elif op == '3':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid option. Please select again.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if con:
            con.close()
            print("Connection closed.")
