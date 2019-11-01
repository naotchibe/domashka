import argparse

from processor import Processor
from readers_and_writers import JsonWriter, XmlWriter
from db_connectors.mysql_db_worker import MysqlWorker

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("arg1")
    parser.add_argument("arg2")
    parser.add_argument("arg3")
    parser.add_argument("host")
    parser.add_argument("user")
    parser.add_argument("name")
    parser.add_argument("password")
    parser.add_argument("charset")
    parser.add_argument("db")

    args = parser.parse_args()
    students_path = args.arg1
    room_path = args.arg2
    type_alex = args.arg3
    writer = JsonWriter() if type_alex == "json" else XmlWriter()
    pr = Processor(
        writer,
        MysqlWorker(host=args.host,
                    user=args.user,
                    name=args.name,
                    password=args.password,
                    db=args.db,
                    charset=args.charset))
    pr.process(room_path, students_path)
