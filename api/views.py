from django.shortcuts import render
from rest_framework.views import APIView
from api.models import todos
from rest_framework.views import Response
from rest_framework import status
import json


def read_todos():
    with open("C:\\Users\\ASHVAD SHAJAN\\PycharmProjects\\django\\todoapi\\api\\todos.json", "r") as f:
        data = json.load(f)
    return data


# Create your views here.

class Todos(APIView):
    def get(self, request, *args, **kwargs):
        data = read_todos()
        return Response({"data": data}, status=status.HTTP_200_OK)


class TodoDetail(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        data = read_todos()
        try:
            todo = [todo for todo in data if todo["id"] == id][0]
            return Response({"todo": todo}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "invalid id"}, status=status.HTTP_400_BAD_REQUEST)

# API/v1/mytodos?userid=1 and completed=True

class MyTodos(APIView):
    def get(self, request, *args, **kwargs):
        print(request.query_params)
        userid = request.query_params.get("userid")
        completed = request.query_params.get("completed")
        print(userid)
        data = read_todos()
        todos = [todo for todo in data if (todo["userId"] == int(userid)) & (todo["completed"] == completed)]
        print(todos)
        return Response({"data": todos})
