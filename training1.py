import pymysql
from contextlib import closing
from pymysql.cursors import DictCursor
import json
import sys
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

    def create_indexes(self):
        raise NotImplementedError


class MysqlWorker(DbWorker):
    def __init__(self):
        self.__drop_students_table()
        self.__drop_rooms_table()
        self.__create_rooms_table()
        self.__create_students_table()

    def get_rooms_and_students(self):
        query = """
        select id, room_name, count(student_id) as students_number
                    from rooms RMS
                    left outer join students STS
                    on RMS.id = STS.room_id
                    group by RMS.id;
        """
        return self.__execute_select_request(query)

    def get_rooms_with_minimal_average_students_age(self):
        query = """
        Select id, room_name from rooms RMS
                    inner join students STS
                    on RMS.id = STS.room_id
                    group by RMS.id
                    order by avg(STS.birthday)
                    limit 5;
        """
        return self.__execute_select_request(query)

    def get_rooms_with_maximum_difference_in_students_age(self):
        query = """
        Select id, room_name from rooms RMS
                    inner join students ST1 on RMS.id = ST1.room_id
                    inner join students ST2 on RMS.id = ST2.room_id
                    group by RMS.id
                    order by max(timestampdiff(second, ST1.birthday, ST2.birthday)) DESC
                    limit 5;
        """
        return self.__execute_select_request(query)

    def get_rooms_with_students_with_different_sex(self):
        query = """
        Select id, room_name from rooms RMS
                    inner join students ST1 on RMS.id = ST1.room_id
                    inner join students ST2 on RMS.id = ST2.room_id
                    where ST1.sex != ST2.sex
                    group by RMS.id;
        
        """
        return self.__execute_select_request(query)

    def add_students(self, students):
        with closing(self.__get_connection()) as conn:
            with conn.cursor() as cursor:
                query = 'INSERT INTO students (student_id, student_name, birthday, sex, room_id) VALUES (%s, %s, %s, %s, %s)'

                def value(n):
                    return n["id"], n["name"], n["birthday"], n["sex"], n["room"]

                values = map(value, students)
                cursor.executemany(query, values)
                conn.commit()

    def add_rooms(self, rooms):
        with closing(self.__get_connection()) as conn:
            with conn.cursor() as cursor:
                query = 'INSERT INTO rooms (id, room_name) VALUES (%s, %s)'

                def value(n):
                    return n["id"], n["name"]
                values = map(value, rooms)
                cursor.executemany(query, values)
                conn.commit()

    def create_indexes(self):
        room_query = 'CREATE INDEX room_id ON task4.rooms(id)'
        student_query = 'CREATE INDEX student_id on task4.students(student_id)'

        self.__execute_request(room_query)
        self.__execute_request(student_query)

    def __create_rooms_table(self):
        query = """
        create table if not exists task4.rooms(
            id int not null,
            room_name varchar(45) not null,
            PRIMARY KEY (id));
        """
        self.__execute_request(query)

    def __create_students_table(self):
        query = """
            create table if not exists task4.students (
            student_id int not null,
            student_name varchar(45) not null,
            birthday date not null, 
            sex varchar(45) not null,
            room_id int,
            primary key(student_id)
            );
        """
        self.__execute_request(query)

    def __drop_rooms_table(self):
        query = """
        DROP TABLE IF EXISTS task4.rooms
         """
        self.__execute_request(query)

    def __drop_students_table(self):
        query = """
        DROP TABLE IF EXISTS task4.students
         """
        self.__execute_request(query)

    def __execute_request(self, query):
        with closing(self.__get_connection()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()

    def __execute_select_request(self, query):
        with closing(self.__get_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def __get_connection(self):
        return pymysql.connect(
            host='localhost',
            user='root',
            password='1111',
            db='task4',
            charset='utf8mb4',
            cursorclass=DictCursor
        )

    def __get_values(self, item):
        return item.values


class Processor():
    def __init__(self, writer: Writer, db_worker: DbWorker):
        self.writer = writer
        self.reader = Reader()
        self.db_worker = db_worker

    def process(self, rooms_fname, students_fname):
        students = self.reader.read(students_fname)
        rooms = self.reader.read(rooms_fname)

        self.db_worker.add_rooms(rooms)
        self.db_worker.add_students(students)

        self.db_worker.create_indexes()

        results = {
            "rooms_and_students": self.db_worker.get_rooms_and_students(),
            "rooms_with_students_with_different_sex": self.db_worker.get_rooms_with_students_with_different_sex(),
            "rooms_with_maximum_difference_in_students_age": self.db_worker.get_rooms_with_maximum_difference_in_students_age(),
            "rooms_with_minimal_average_students_age": self.db_worker.get_rooms_with_minimal_average_students_age(),
        }

        self.writer.write("alex", results)

def main():
    students_path = sys.argv[1]
    room_path = sys.argv[2]
    type_alex = sys.argv[3]
    writer = JsonWriter() if type_alex == "json" else XmlWriter()
    pr = Processor(writer, MysqlWorker())
    pr.process(room_path, students_path)


if __name__ == '__main__':
    main()
