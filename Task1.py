import json
import sys
import dicttoxml

class Reader():
    def read(self, file):
        with open(file) as json_file: 
            return json.load(json_file)

class Writer():
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

class Processsor():
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
                student_room["students"].append({"id": student['id'], "name": student['name']})
        self.writer.write("alex", rooms)       

def main():
    students_path = sys.argv[1]
    room_path = sys.argv[2]
    type_alex = sys.argv[3]
    writer = JsonWriter() if type_alex == "json" else XmlWriter()
    pr = Processsor(writer)
    pr.process(room_path, students_path)

if __name__ == '__main__':
    main()


