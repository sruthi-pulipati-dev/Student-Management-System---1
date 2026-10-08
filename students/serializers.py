from rest_framework import serializers 
from .models import Student
from rest_framework.exceptions import ValidationError

class StudentSerializer(serializers.ModelSerializer):
    class Meta :
        model = Student
        fields = "__all__"
        read_only_fields = ["joined_at"]

    def validate(self, attrs):
        if self.instance is not None and 'student_id' in attrs and attrs['student_id'] != self.instance.student_id:
            raise ValidationError("Student id cannot be updated")
        return attrs

    def validate_first_name(self, value):
        if(any((not char.isalpha() and char != ' ') for char in value)):
            raise ValidationError("First name should only have alphabets and spaces")
        return value 

    def validate_last_name(self, value):
        if(any((not char.isalpha() and char != ' ') for char in value)):
            raise ValidationError("Last name should only have alphabets and spaces")
        return value
    
    def validate_mobile_no(self, value):
        if(any(not char.isdigit() for char in value)) :
            raise ValidationError("Mobile no only contains digits")
        if(len(value) != 10):
            raise ValidationError("Mobile no should have exactly 10 digits")
        return value
            


    