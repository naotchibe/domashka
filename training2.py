import json
import argparse
import dicttoxml


class Reader:
    def read(self, file):
        with open(file) as json_file:
            return json.load(json_file)


class Writer:
    def write(self, file, data):
        raise NotImplementedError


class JsonWriter(Writer):
    def write(self, file, data):
        with open(file, 'w') as output:
            json.dump(data, output)


class XmlWriter(Writer):
    def write(self, file, data):
        with open(file, "w") as xml_file:
            xml = dicttoxml.dicttoxml(data)
            decode = xml.decode()
            xml_file.write(decode)


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


class MySqlWorker(DbWorker):
    def __init__(self):
        self.__drop_students_table()
        self.__drop_rooms_table()
        self.__create_rooms_table()
        self.__create_students_table()

    def get_rooms_and_students(self):
        query = ""
        return self.__execute_select_reqest(query)

    def __execute_select_reqest(self):
        with closing(self.__get_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()


class Processsor:
    def __init__(self, writer: Writer):
        self.writer = writer
        self.reader = Reader()

    def process(self, rooms_fname, students_fname):
        students = self.reader.read(students_fname)
        rooms = self.reader.read(rooms_fname)
        room_dict = {x["id"]: x for x in rooms}
        for student in students:
            student_room = room_dict.get(student["room"])
            if student_room:
                if "students" not in student_room.keys():
                    student_room["students"] = []
                student_room["students"].append(
                    {"id": student['id'], "name": student['name']})
        self.writer.write("alex", rooms)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("arg1")
    parser.add_argument("arg2")
    parser.add_argument("arg3")
    args = parser.parse_args()
    students_path = args.arg1
    room_path = args.arg2
    type_alex = args.arg3
    writer = JsonWriter() if type_alex == "json" else XmlWriter()
    pr = Processsor(writer)
    pr.process(room_path, students_path)


if __name__ == '__main__':
    main()
