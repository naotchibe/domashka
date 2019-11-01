from db_connectors import DbWorker
from readers_and_writers import Reader, Writer


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
            "rooms_and_students":
            self.db_worker.get_rooms_and_students(),
            "rooms_with_students_with_different_sex":
            self.db_worker.get_rooms_with_students_with_different_sex(),
            "rooms_with_maximum_difference_in_students_age":
            self.db_worker.get_rooms_with_maximum_difference_in_students_age(),
            "rooms_with_minimal_average_students_age":
            self.db_worker.get_rooms_with_minimal_average_students_age(),
        }

        self.writer.write("alex", results)
