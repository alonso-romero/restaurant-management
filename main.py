import os
import time

class Timer:
    def __init__(self, table_number):
        self.table_number = table_number
        self.start_time = None

    def assign_table(self):
        self.start_time = time.time()

    def check_time(self):
        if self.start_time is None:
            return 0
        else:
            elapsed_time = (time.time() - self.start_time) / 60
            return elapsed_time

class Server:
    def __init__(self, name):
        self.name = name
        self.tables_handled = 0

    def can_handle_more_tables(self):
        return self.tables_handled <= 6
    
    def assign_table(self):
        if self.can_handle_more_tables():
            self.tables_handled += 1
        else:
            raise Exception(f"{self.name} cannot handle any more tables!")
        
class Restaurant:
    def __init__(self):
        self.servers = []
        self.tables = {f'{section}{number}': {'server': None, 'timer': Timer(f'{section}{number}')}
                       for section in 'ABCD' for number in range(1, 6)}
        self.clear_screen()

    def clear_screen(self):
        # For Windows
        if os.name == 'nt':
            _ = os.system('cls')
        # For macOS and Linux
        else:
            _ = os.system('clear')

    def get_integer_input(self, prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Invalid input.")
                continue

    def exit_verify(self):
        while True:
            exit_screen = input("Type X to go back to the menu: ").upper()
            if exit_screen == "X":
                self.clear_screen()
                break
            else:
                print("Invalid input.")

    def mainmenu(self):
        print("1.) Clock In Servers")
        print("2.) View Servers")
        print("3.) Calculate Wait Time")
        print("4.) View Table Times")
        print("5.) Assign Table")
        print("6.) Exit")

    def clock_in_servers(self):
        self.clear_screen()
        while True:
            server_name = input("Enter server name (or 'done' to finish): ")
            if server_name.lower() == "done":
                self.clear_screen()
                break
            if server_name not in [server.name for server in self.servers]:
                self.servers.append(Server(server_name))
                print(f"{server_name} clocked in\n")
            else:
                print(f"{server_name} is already clocked in.")

    def view_servers(self):
        self.clear_screen()
        if self.servers:
            print("Servers clocked in:")
            for server in self.servers:
                print(f" - {server.name}")
        else:
            print("No servers are clocked in.")
        self.exit_verify()

    def calculate_wait_time(self):
        all_servers_full = all(server.tables_handled >= 6 for server in self.servers)
        any_open_tables = any(table['server'] is None for table in self.tables.values())

        if any_open_tables and not all_servers_full:
            return 0
        
        occupied_tables = [table for table in self.tables.values() if table['server'] is not None]
        occupied_count = len(occupied_tables)

        wait_times = [10, 15, 20, 30, 45, 60, 90]
        index = min(occupied_count - 1, len(wait_times) - 1)
        return wait_times[index]

    def view_table_times(self):
        self.clear_screen()
        while True:
            for table, info in self.tables.items():
                elapsed_time = info['timer'].check_time()
                if info['server']:
                    print(f"{table}: {elapsed_time:.2f} minutes ({info['server'].name})")
                else:
                    print(f"{table}: -")
            refresh = input("Press 'r' to update times, or 'x' to exit: ").lower()
            if refresh == 'r':
                self.clear_screen()
                continue
            elif refresh == 'x':
                break
            else:
                print('Invalid input')

    def assign_table(self):
        self.clear_screen()
        while True:
            party_size = self.get_integer_input("Enter party size (or 0 to exit): ")
            if party_size == 0:
                self.clear_screen()
                break

            suitable_tables = []

            if 7 <= party_size <= 12:
                suitable_tables = [
                    ['D2', 'D3'], ['D4', 'D5'], ['A3', 'A4'], ['A6', 'A7'], ['A8', 'A9']
                ]

            elif 13 <= party_size <= 24:
                suitable_tables = [
                    ['D2', 'D3', 'D4', 'D5'], ['A6', 'A7', 'A8', 'A9']
                ]

            else:
                suitable_tables = [[table] for table in self.tables if self.tables[table]['server'] is None]

            for tables in suitable_tables:
                if all(self.tables[table]['server'] is None for table in tables):
                    server_choice = input("Enter server: ")
                    server_obj = next((server for server in self.servers if server.name == server_choice), None)
                    if server_obj and server_obj.can_handle_more_tables():
                        for table in tables:
                            self.tables[table]['server'] = server_obj
                            self.tables[table]['timer'].assign_table()
                        server_obj.assign_table()
                        print(f"Assigned tables {', '.join(tables)} to {server_choice}")
                        break
                else:
                    if not server_obj:
                        print("Invalid server name")
                    else:
                        print(f"{server_choice} cannot handle any more tables.")
                    break

            else:
                print("No suitable tables available.")

    def run(self):
        while True:
            self.clear_screen()
            print("========== Restaurant Host System ==========\n")
            self.mainmenu()
            choice = self.get_integer_input("\nEnter your choice: ")

            if choice == 1:       # Clock in Servers
                self.clock_in_servers()
            elif choice == 2:     # View Servers
                self.view_servers()
            elif choice == 3:     # Calculate Wait Time
                wait_time = self.calculate_wait_time()
                print(f"Current wait time: {wait_time} minutes")
                self.exit_verify()
            elif choice == 4:     # View Table Times
                self.view_table_times()
            elif choice == 5:     # Assign Table
                self.assign_table()
            elif choice == 6:
                self.clear_screen()
                break
            else:
                print("Invalid input.")

# Run the restaurant system
restaurant = Restaurant()
restaurant.run()