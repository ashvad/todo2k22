from django.shortcuts import render
from todoapp.serializers import TodoSerializer, UserSerializer, LoginSerializer
from todoapp.models import Todos
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins, viewsets
from django.contrib.auth.models import User
from rest_framework import authentication, permissions


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


class TodoDetail(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        todo = Todos.objects.get(id=id)
        serializers = TodoSerializer(todo)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        todo = Todos.objects.get(id=id)
        serializer = TodoSerializer(data=request.data, instance=todo)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        todo = Todos.objects.get(id=id)
        todo.delete()
        return Response({"msg": "deleted"}, status=status.HTTP_200_OK)


# __________________________________________________________________________________________

class TodoMisxinList(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    serializer_class = TodoSerializer
    queryset = Todos.objects.all()
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TodoMixinDetail(generics.GenericAPIView,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# ________________________________________________________________________________________

class TodoViewsets(viewsets.ViewSet):
    serializer_class = TodoSerializer
    model = Todos

    def list(self, request):
        todos = self.model.objects.all()
        serializer = self.serializer_class(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        todo = self.model.objects.get(id=id)
        serializer = self.serializer_class(data=request.data, instance=todo)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        print(kwargs)
        id = kwargs.get("pk")
        todo = self.model.objects.get(id=id)
        serializer = self.serializer_class(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        todo = self.model.objects.get(id=id)
        todo.delete()
        return Response({"msg": "deleted"}, status=status.HTTP_200_OK)


# _________________________________________________________________________________________

class TodoModelViewset(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todos.objects.all()
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewsets(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()



# ___________________________________________________________________________________________

class SigninView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return Response({"msg": "access granted"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors)
