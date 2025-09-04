def coursestudents(students, course_name):
    return [student.name for student in students if course_name in student.courses]
