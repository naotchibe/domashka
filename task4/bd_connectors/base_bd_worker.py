class DbWorker:

    def get_rooms_and_students(self):
        raise NotImplementedError

    def get_rooms_with_minimal_average_students_age(self):
        raise NotImplementedError

    def get_rooms_with_maximum_difference_in_students_age(self):
        raise NotImplementedError

    def get_rooms_with_students_with_different_sex(self):
        raise NotImplementedError

    def add_students(self, students):
        raise NotImplementedError

    def add_rooms(self, rooms):
        raise NotImplementedError

    def create_indexes(self):
        raise NotImplementedError
