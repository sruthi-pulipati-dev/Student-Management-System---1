from django.shortcuts import render
from rest_framework.decorators import api_view 
from .models import Student
from rest_framework.response import Response
from rest_framework import status
from .utils import get_student_info, set_student_info, set_partial_student_info, check_all_fields, validate_incoming_data
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def students(request):

    if(request.method == 'POST'):
        try :
            data = request.data 
            validate_incoming_data(data)
            student = Student(**data)
            student.full_clean()
            student.save()
            response_data = get_student_info(student)
            logger.info('Student created')
            return Response({'success': True, 'data': response_data}, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            logger.error('Error while creating student')
            return Response({'success': False, 'errors': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    elif(request.method == 'GET'):
        response_data = []
        params = request.query_params.dict()
        params.pop('format', None)

        if(params):
            students = Student.objects.filter(**params)
        else :
            students = Student.objects.all()

        for student in students:
            response_data.append(get_student_info(student))
        logger.info('Got all students information')
        return Response({'success': True, 'data': response_data}, status=status.HTTP_200_OK)
        

@api_view(['GET','PUT','PATCH','DELETE'])
def update_students(request, student_id):

    student = None
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist as error:
        logger.error('Error while getting student info')
        return Response({'success': False, 'errors':str(error)}, status=status.HTTP_404_NOT_FOUND)
    
    if(request.method=='GET'):
        response_data = get_student_info(student)
        logger.info('Got student info')
        return Response({'success':True, 'data': response_data}, status=status.HTTP_200_OK)

    elif(request.method == 'PUT'):
        data = request.data 
        all_fields = check_all_fields(data)

        if(not all_fields):
            logger.error('All required fields for put request are not sent')
            return Response({'success': False, 'errors': 'All required fields for put request are not sent'}, status=status.HTTP_400_BAD_REQUEST)
        
        try : 
            validate_incoming_data(data)
            set_student_info(student, data)
            response_data = get_student_info(student)
            logger.info('Updated student info')
            return Response({'success': True, 'data' : response_data}, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response({'success': False, 'errors': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    elif(request.method == 'PATCH'):
        try :
            data = request.data 
            validate_incoming_data(data)
            set_partial_student_info(student, data)
            response_data = get_student_info(student)
            logger.info('Updated student info')
            return Response({'success':True, 'data': response_data}, status=status.HTTP_200_OK)
        except ValidationError as error:
            logger.error('Getting error while updating the student info')
            return Response({'success': False, 'errors': str(error)}, status=status.HTTP_400_BAD_REQUEST)


    elif(request.method == 'DELETE'):
        student.delete()
        logger.info('Student deleted successfully')
        return Response({'success':True}, status=status.HTTP_200_OK)




        