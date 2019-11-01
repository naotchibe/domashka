import dicttoxml
import json


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
