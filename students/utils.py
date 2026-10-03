from django.core.exceptions import ValidationError

student_data_fields = ["student_id", "first_name", "last_name", "course", "gender", "mobile_no", "date_of_birth", "joined_at"]
required_fields = ["first_name", "last_name", "course", "gender", "mobile_no", "date_of_birth"]

def validate_incoming_data(data):
    for key, value in data.items() :
        if(not isinstance(value, str)) :
            raise ValidationError(f"{key} must be a string")

def check_all_fields(data):
    for field in required_fields:
        if field not in data:
            return False
    return True

def get_student_info(student):
    response_data = {}
    for field in student_data_fields:
        response_data[field] = getattr(student, field)
    return response_data

def set_student_info(student, kwargs):
    for attr in required_fields:
        setattr(student, attr, kwargs[attr])
    student.full_clean()
    student.save()

def set_partial_student_info(student, kwargs):
    for attr, value in kwargs.items():
        setattr(student, attr, value)
    student.full_clean()
    student.save()
