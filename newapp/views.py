from django.shortcuts import render
from .models import Students,Marks
from rest_framework.decorators import api_view
from django.http import JsonResponse
from datetime import datetime
import pandas as pd
from student import connection
from rest_framework import viewsets,status
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404

@api_view(['POST'])
def check(request):
    data=Students.objects.filter().values()
    return JsonResponse(list(data), safe=False)


@api_view(['POST'])
def create_student(request):
    create_student=Students.objects.create(
        name=request.data['name'],
        age=request.data['age'],
        address=request.data['address'],
        created_timestam=datetime.now()
    )
    if create_student.roll_number>0:
        return JsonResponse("student created successfully", safe=False)
    else:
        return JsonResponse("unabel to create student", safe=False)


@api_view(['POST'])
def create_marks(request):
    try:
        data_check=Marks.objects.filter(roll_number=request.data['roll_number'])
        if not data_check.exists():
            create_marks=Marks.objects.create(
                roll_number=Students.objects.get(roll_number=request.data['roll_number']),
                english=request.data['english'],
                tamil=request.data['tamil'],
                maths= request.data['maths']
            )
            if create_marks.id>0:
                return JsonResponse("Marks added successfully", safe=False)
            else:
                return JsonResponse("unabel added Marks", safe=False)
        else:
            update_marks=data_check.update(
                roll_number=Students.objects.get(roll_number=request.data['roll_number']),
                english=request.data['english'],
                tamil=request.data['tamil'],
                maths= request.data['maths']
            )
            if update_marks>0:
                return JsonResponse("Marks updated successfully", safe=False)
            else:
                return JsonResponse("unabel updated Marks", safe=False)

    except Exception as e:
        print('r',e)

@api_view(['POST'])
def data_retrive(request):
    con=connection.connection_data_defualt(request)
    roll_number=request.data['roll_number']
    query="""select st.name,st.age,pa.fathers_name,CASE
        WHEN mr.english isnull THEN 'RA' else mr.english::text End
        from "Master".studnet st
        left join "Master".marks mr on st.roll_number = mr.roll_number
        left join "Master".parents pa on st.roll_number = pa.roll_number
        where st.roll_number={}""".format(roll_number)
    data=connection.cursor_data(con,query)
    return JsonResponse(data,safe=False)
    




class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Students.objects.all().order_by('-roll_number')
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    # Override other actions to disallow them
    def create(self, request):
        return Response({'message': 'Create action is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        return Response({'message': 'Retrieve action is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response({'message': 'Update action is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response({'message': 'Partial update action is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response({'message': 'Destroy action is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class newuserviewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer  
    queryset = Students.objects.all().order_by('roll_number')


    @action(detail=True, methods=['put'], name='update')
    def update_student(self, request, pk=None):
        student = self.get_object()
        serializer = StudentSerializer(student, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=True, methods=['get'], name='get_student')
    # def get_student(self, request, pk=None):
    #     student = self.get_object()
    #     serializer = StudentSerializer(student)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], name='get_student')
    def get_student(self, request, pk=None):
        try:
            student = Students.objects.filter(roll_number=pk)
            data = student.values()
            if data.exists():
                return JsonResponse(list(data), safe=False,status=status.HTTP_200_OK)
            else:
                return JsonResponse("No records found", safe=False)
        except Students.DoesNotExist:
            return JsonResponse("Unabel to perform action", safe=False)