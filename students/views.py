from django.shortcuts import render
from rest_framework.decorators import api_view 
from .models import Student, Faculty, Guardian
from rest_framework.response import Response
from rest_framework import status
import logging
from django.core.exceptions import ValidationError
from .serializers import StudentSerializer, FacultySerializer, GuardianSerializer

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def students(request):

    if(request.method == 'POST'):
        
        serializer = StudentSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            logger.info('Student created')
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
    
        else:
            logger.error('Error while creating student')
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif(request.method == 'GET'):
        params = request.query_params.dict()
        params.pop('format', None)

        try:
            if(params):
                students = Student.objects.filter(**params)
            else :
                students = Student.objects.all()

            serializer = StudentSerializer(students, many=True)
            logger.info('Got all students information')
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Student.DoesNotExist as error :
            logger.info("Student object does not exits")
            return Response({'success':False, 'errors':str(error)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','PATCH','DELETE'])
def update_students(request, student_id):

    student = None
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist as error:
        logger.error('Error while getting student info')
        return Response({'success': False, 'errors':str(error)}, status=status.HTTP_404_NOT_FOUND)
    
    if(request.method=='GET'):
        serializer = StudentSerializer(student)
        logger.info('Got student info')
        return Response({'success':True, 'data': serializer.data}, status=status.HTTP_200_OK)

    elif(request.method == 'PUT'):
        
        try : 
            serializer = StudentSerializer(instance=student, data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                logger.info('Updated student info')
                return Response({'success': True, 'data' : serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.info("Failed while updating student info")
                return Response({'success':False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as error:
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif(request.method == 'PATCH'):
        try :
            serializer = StudentSerializer(instance=student, data=request.data, partial=True)
            if(serializer.is_valid()):
                serializer.save()
                logger.info('Updated student info')
                return Response({'success':True, 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.info("Failed while updating student info")
                return Response({'success':False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
        except ValidationError as error:
            logger.error('Getting error while updating the student info')
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    elif(request.method == 'DELETE'):
        try:
            student.delete()
            logger.info('Student deleted successfully')
            return Response({'success':True}, status=status.HTTP_200_OK)
        except Exception as error:
            logger.error("Error while deleting the student")
            return Response({'success':False, 'errors':str(error)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def faculty(request):

    if(request.method == 'GET') :

        try :
            params = request.query_params.dict()
            if(params):
                faculty_objs = Faculty.objects.filter(**params)
            else :
                faculty_objs = Faculty.objects.all()
            serializer = FacultySerializer(faculty_objs, many=True)
            logger.info("Got faculty info")
            return Response({'success':True, 'data': serializer.data}, status=status.HTTP_200_OK)

        except Faculty.DoesNotExist as error:
            logger.info("Faculty object does not exits")
            return Response({'success':False, 'errors':str(error)}, status=status.HTTP_400_BAD_REQUEST)
    
    elif(request.method == 'POST'):
        serializer = FacultySerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({'success':True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success':False, 'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def guardian(request):
    if(request.method == 'GET'):
        try:
            params = request.query_params.dict()
            if(params):
                guardian_objs = Guardian.objects.filter(**params)
            else :
                guardian_objs = Guardian.objects.all()
            serializer = GuardianSerializer(guardian_objs, many=True)
            return Response({'success':True, 'data': serializer.data}, status=status.HTTP_200_OK)

        except Guardian.DoesNotExist as error :
            logger.info("Guardian object does not exits")
            return Response({'success':False, 'errors':str(error)}, status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='POST'):
        serializer = GuardianSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({'success':True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success':False, 'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
