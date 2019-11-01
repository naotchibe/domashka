from base_bd_worker import DbWorker
from contextlib import closing
from pymysql.cursors import DictCursor
from pymysql import connect


class MysqlWorker(DbWorker):
    def __init__(self, **kwargs):
        try:
            self.host = kwargs["host"]
            self.name= kwargs["name"]
            self.password=kwargs["password"]
            self.db=kwargs["db"]
            self.charset=kwargs["charset"]               
            self.user=kwargs["user"]
        except KeyError as e:
            raise Exception("Wrong params from console line")

        self.__drop_students_table()
        self.__drop_rooms_table()
        self.__create_rooms_table()
        self.__create_students_table()
        self.host = params.host

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
                    order by max(timestampdiff(second, ST1.birthday,\
                         ST2.birthday)) DESC
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
                query = 'INSERT INTO students (student_id, student_name, \
                    birthday, sex, room_id) VALUES (%s, %s, %s, %s, %s)'

                def value(n):
                    return n["id"], n["name"], n["birthday"], n["sex"], n[
                        "room"]

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
        return connect(host=self.host,
                       user=self.user,
                       password=self.password,
                       db=self.db,
                       charset=self.charset,
                       cursorclass=DictCursor)

    def __get_values(self, item):
        return item.values
