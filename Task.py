import pprint as pp

students = [
    {
        'id': 1,
        'name': 'Nikita #1',
        'room': 1
    },
    {
        'id': 2,
        'name': 'Nikita #2',
        'room': 1
    },
    {
        'id': 3,
        'name': 'Nikita #3',
        'room': 2
    },
    {
        'id': 4,
        'name': 'Nikita #4',
        'room': 2
    },
    {
        'id': 5,
        'name': 'Nikita #5',
        'room': 2
    },
    {
        'id': 6,
        'name': 'Nikita #6',
        'room': 2
    },
    {
        'id': 7,
        'name': 'Nikita #7',
        'room': 3
    }
]

rooms = [
    {
        'id': 1,
        'name': 'Room #1',
        'students': []
    },
    {
        'id': 2,
        'name': 'Room #2',
        'students': []
    },
    {
        'id': 42,
        'name': 'Room #42',
        'students': []
    }
] 
room_dict={ x["id"]:x for x in rooms}
for student in students:
    student_room = room_dict.get(student["room"])
    if student_room:
        student_room["students"].append({"id": student['id'], "name": student['name'] })
pp.pprint(rooms)        
