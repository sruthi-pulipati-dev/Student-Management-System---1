from django.db import models

class Student(models.Model):

    class Courses(models.TextChoices):
        CSE = "CSE", "CSE"
        AIML = "AIML", "AIML"
        DS = "DS", "DS"
        CIVIL = "CIVIL", "CIVIL"
        MECH = "MECH", "MECH"
        EEE = "EEE", "EEE"
        ECE = "ECE", "ECE"
        IT = "IT", "IT"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"
        
    student_id = models.CharField(max_length=10, null=False ,blank=False, unique=True)
    first_name = models.CharField(max_length=50, null=False ,blank=False)
    last_name = models.CharField(max_length=50, null=False ,blank=False)
    course = models.CharField(max_length=20, null=False ,blank=False, choices=Courses.choices)
    gender = models.CharField(max_length=10, null=False ,blank=False, choices=Gender.choices)
    mobile_no = models.CharField(max_length=10, null=False ,blank=False, unique=True)
    date_of_birth = models.DateField(null=False ,blank=False)
    joined_at = models.DateField(null=False ,blank=False, auto_now_add=True)
