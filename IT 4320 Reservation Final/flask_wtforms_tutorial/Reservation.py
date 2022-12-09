class Reservation:
    def __init__(self):
        self.cost_matrix = self.__get_cost_matrix()
        self.reservations = self.__load_reservations()
        self.bus_map = self.__get_bus_map()
        
    def __get_cost_matrix(self):

        cost_matrix = [[100, 75, 50, 100] for row in range(12)]
        return cost_matrix

    def __load_reservations(self):

        reservations = []
        try:
            with open("./reservations.txt") as reservation_file:
                for reservation in reservation_file:
                    reservation_data = reservation.split(",")
                    reservation_dict = {
                        "first_name": reservation_data[0].strip(),
                        "row": int(reservation_data[1]),
                        "seat": int(reservation_data[2]),
                        "e-ticket": reservation_data[3].strip()
                    }
                    reservations.append(reservation_dict)
        except:
            raise Exception("💥 ERROR: Reservation database unavailable.  Please try again later or contact an administrator if the problem persists. 💥")
        else:
            return reservations

    def __get_bus_map(self):

        seat_list = [['O' for col in range(4)] for row in range(12)]

        for i in range(len(self.reservations)):
            seat_row = self.reservations[i]['row']
            seat = self.reservations[i]['seat']
            for _ in range(len(seat_list[0])):
                seat_list[seat_row][seat] = 'X'

        return seat_list

    def __generate_eticket(self) -> str:

        name_array = [char for char in self.first_name]
        course_array = [char for char in "INFOTC4320"]

        merged = []
        if len(course_array) > len(name_array):
            for i in range(len(course_array)):
                if i < len(name_array):
                    merged.append(name_array[i])
                    merged.append(course_array[i])
                else:
                    merged.append(course_array[i])
        else:
            for i in range(len(name_array)):
                if i < len(course_array):
                    merged.append(name_array[i])
                    merged.append(course_array[i])
                else:
                    merged.append(name_array[i])
        return "".join(merged)

    def __check_seat_availability(self, row:int, seat:int) -> bool:
 
        for i in range(len(self.reservations)):
            if row == self.reservations[i]['row']:
                if seat == self.reservations[i]['seat']:
                    return False
        return True

    def __persist_reservation(self) -> bool:

        try:
            with open("./reservations.txt", "a") as reservation_file:
                reservation = f"{self.first_name}, {self.row}, {self.seat}, {self.e_ticket}\n"
                reservation_file.write(reservation)
                return True
        except:
            return False
    
    def make_reservation(self, first_name:str, last_name:str, row:int, seat:int) -> str:

        total_seats = 48
        seats_remaining = total_seats - len(self.reservations)

        if seats_remaining != 0:
            self.first_name = first_name.title()
            self.last_name = last_name.title()
            self.row = row - 1
            self.seat = seat - 1
            if self.__check_seat_availability(self.row, self.seat):
                self.e_ticket = self.__generate_eticket()
                if self.__persist_reservation():
                    self.reservations.append({
                        "first_name": self.first_name,
                        "row": self.row,
                        "seat": self.seat,
                        "e-ticket": self.e_ticket
                    })
                    self.bus_map = self.__get_bus_map()
                    return f"Congrats {self.first_name.title()}! Row:  {row} Seat:  {seat} is now reserved for you!  Enjoy your break!!!"
                else:
                    raise Exception("ERROR: Reservation database unavailable. ")
            else:
                raise Exception(f"\nRow:  {row} Seat:  {seat}, is already assigned/taken... Please choose a seat that is available.....\n")
        else:
            raise Exception("Apologizes.. This bus is currently full...")

    def calculate_total_sales(self) -> float:

        total = 0.0

        for row in range(len(self.bus_map)):
            for seat in range(len(self.bus_map[0])):
                if self.bus_map[row][seat] == 'X':
                    total += self.cost_matrix[row][seat]

        return total