from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .permissions import IsAuthenticatedOrCreate
from rest_framework import status, generics as g
from rest_framework.response import Response


# Create your views here.
# https://www.madewithtea.com/simple-todo-api-with-django-and-oauth2.html
# https://yeti.co/blog/oauth2-with-django-rest-framework/



class RegistrationView(APIView):

    permission_classes = ()

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data) 
        # Check format and unique constraint 
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        data = serializer.data
        u = User.objects.create(username=data['username'])
        u.set_password(data['password'])
        u.save()
        # Create OAuth2 client
        name = u.username
        client = Client(user=u, name=name, url='' + name,\
                        client_id=name, client_secret='', client_type=1)
        client.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TodosView(APIView):

    permission_classes = (IsAuthenticated,) # explicit

    def get(self, request):
        todos = Todo.objects.filter(owner=request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            owner = request.user
            t = Todo(owner=owner, description=data['description'], done=False)
            t.save()
            request.data['id'] = t.pk # return id
            return Response(request.data, status=status.HTTP_201_CREATED)

    def put(self, request, todo_id):
        serializer = TodoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            desc = data['description']
            done = data['done']
            t = Todo(id=todo_id, owner=request.user, description=desc,\
                    done=done, updated=datetime.now())
            t.save()
            return Response(status=status.HTTP_200_OK)



class SignUp(g.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)



