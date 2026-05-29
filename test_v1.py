import json
import os
# from datetime import datetime

# File paths
ORGANIZERS_FILE = "organizers.json"
MEMBERS_FILE = "members.json"
EVENTS_FILE = "events.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def register_user(user_type):
    name = input("Enter full name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    users = load_data(ORGANIZERS_FILE if user_type == "organizer" else MEMBERS_FILE)
    # users.append({"Full Name": name, "Email": email, "Password": password})
    if user_type == "member":
        users.append({
        "Full Name": name,
        "Email": email,
        "Password": password,
        "Wallet": 0
    })
    else:
        users.append({
        "Full Name": name,
        "Email": email,
        "Password": password
    })
    save_data(ORGANIZERS_FILE if user_type == "organizer" else MEMBERS_FILE, users)
    print("Registration successful!")

def login():
    email = input("Enter email: ")
    password = input("Enter password: ")
    for user_type, file in [("organizer", ORGANIZERS_FILE), ("member", MEMBERS_FILE)]:
        users = load_data(file)
        for user in users:
            if user["Email"] == email and user["Password"] == password:
                print(f"Welcome {user['Full Name']}!")
                return user_type, user
    print("Invalid credentials!")
    return None, None

def view_events(show_details=False):
    events = load_data(EVENTS_FILE)
    print("\nEvents:")
    for event in events:
        print(f"{event['ID']} - {event['Name']} ({event['Start Date']} {event['Start Time']})")
        if show_details:
            print(f"  Organizer: {event['Organizer']}")
            print(f"  Seats Available: {event['Seats Available']}/{event['Capacity']}")
    
def add_event(organizer):

    events = load_data(EVENTS_FILE)

    event_name = input("Enter event name: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    start_time = input("Enter start time (HH:MM): ")

    end_date = input("Enter end date (YYYY-MM-DD): ")
    end_time = input("Enter end time (HH:MM): ")

    capacity = int(input("Enter seat capacity: "))
    seat_price = int(input("Enter seat price: "))

    event_id = f"EVT{len(events)+1}"

    event = {
        "ID": event_id,
        "Name": event_name,
        "Organizer": organizer["Full Name"],
        "Start Date": start_date,
        "Start Time": start_time,
        "End Date": end_date,
        "End Time": end_time,
        "Users Registered": [],
        "Capacity": capacity,
        "Seats Available": capacity,
        "Seat Price": seat_price
    }

    events.append(event)

    save_data(EVENTS_FILE, events)

    print("Event added successfully!")

def topup_wallet(member):

    amount = int(input("Enter amount to top up: "))

    members = load_data(MEMBERS_FILE)

    for m in members:

        if m["Email"] == member["Email"]:
            m["Wallet"] += amount
            member["Wallet"] = m["Wallet"]

    save_data(MEMBERS_FILE, members)

    print(f"Wallet updated! Current Balance: {member['Wallet']}")

def book_event(member):

    events = load_data(EVENTS_FILE)

    view_events()

    event_id = input("Enter Event ID to book: ")

    for event in events:

        if event["ID"] == event_id:

            if event["Seats Available"] <= 0:
                print("Housefull!")
                return

            if member["Wallet"] < event["Seat Price"]:
                print("Insufficient wallet balance!")
                return

            event["Users Registered"].append(member["Full Name"])

            event["Seats Available"] -= 1

            member["Wallet"] -= event["Seat Price"]

            # Update member wallet in file
            members = load_data(MEMBERS_FILE)

            for m in members:
                if m["Email"] == member["Email"]:
                    m["Wallet"] = member["Wallet"]

            save_data(MEMBERS_FILE, members)
            save_data(EVENTS_FILE, events)

            print("Booking successful!")
            print("Remaining Wallet:", member["Wallet"])

            return

    print("Invalid Event ID!")

def main():
    while True:
        print("1. Register as Organizer\n2. Register as Member\n3. Login\n4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            register_user("organizer")
        elif choice == "2":
            register_user("member")
        elif choice == "3":
            user_type, user = login()
            if user_type == "organizer":
                while True:
                    # print("\n1. View Events\n2. Logout")
                    print("\n1. View Events\n2. Add Event\n3. Logout")
                    sub_choice = input("Choose an option: ")
                    if sub_choice == "1":
                        view_events(show_details=True)
                    # elif sub_choice == "2":
                    #     break
                    elif sub_choice == "2":
                        add_event(user)

                    elif sub_choice == "3":
                        break
            elif user_type == "member":
                while True:
                    # print("\n1. View Events\n2. Logout")
                    print("\n1. View Events\n2. Topup Wallet\n3. Book Event\n4. Logout")
                    sub_choice = input("Choose an option: ")
                    if sub_choice == "1":
                        view_events(show_details=True)
                    # elif sub_choice == "2":
                    #     break
                    elif sub_choice == "2":
                        topup_wallet(user)

                    elif sub_choice == "3":
                        book_event(user)

                    elif sub_choice == "4":
                        break
        elif choice == "4":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
