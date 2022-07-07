from django.shortcuts import render
from todoapp.serializers import TodoSerializer
from todoapp.models import Todos
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class TodoCreateView(APIView):
    def get(self, request, *args, **kwargs):
        todos = Todos.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
