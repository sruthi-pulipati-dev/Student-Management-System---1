from django.db import models

class Faculty(models.Model):
    class Subject(models.TextChoices):
        MATHS = "maths", "Maths"
        PHYSICS = 'physics', 'Physics'
        CHEMISTRY = 'chemistry', 'Chemistry'
        SCIENCE = 'science', 'Science'
        HISTORY = 'history', 'History'

    name = models.CharField(max_length=100, blank=False, null=False)
    subject = models.CharField(max_length=10, choices = Subject.choices, blank=False, null=False)
    experience = models.IntegerField(blank=False, null=False)

class Guardian(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)

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
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE,blank=True, null=True)
    guardian = models.OneToOneField(Guardian, on_delete=models.CASCADE, blank=True, null=True)



