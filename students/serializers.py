from rest_framework import serializers 
from .models import Student, Guardian, Faculty
from rest_framework.exceptions import ValidationError
from django.db import transaction


class FacultySerializer(serializers.ModelSerializer):
    class Meta : 
        model = Faculty
        fields = "__all__"

class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    
    faculty = FacultySerializer()
    guardian = GuardianSerializer()

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

    def create(self, validated_data):

        faculty_data = validated_data.pop('faculty')
        guardian_data = validated_data.pop('guardian')
        
        with transaction.atomic():
            faculty, _ = Faculty.objects.get_or_create(**faculty_data)
            guardian = Guardian.objects.create(**guardian_data)

            student = Student.objects.create(faculty = faculty, guardian=guardian, **validated_data)
        return student

    def update(self, instance, validated_data):
        faculty_data = validated_data.pop('faculty', None)
        guardian_data = validated_data.pop('guardian', None)

        with transaction.atomic():

            if faculty_data is not None :
                faculty = instance.faculty

                for key, value in faculty_data.items() :
                    setattr(faculty, key, value)
                faculty.save()

            if guardian_data is not None :
                guardian = instance.guardian

                for key, value in guardian_data.items():
                    setattr(guardian, key, value)
                guardian.save()
            
            for key, value in validated_data.items() :
                setattr(instance, key, value)

            instance.save()

        return instance
            

    