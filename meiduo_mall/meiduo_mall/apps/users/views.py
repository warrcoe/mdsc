from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from .serializers import CreateUserSerializer

# Create your views here.
# 用户名验证
class UsernameCountView(APIView):
    '''
    用户名验证
    '''

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        data = {
            'username': username,
            'count':count
        }
        return Response(data)

# 手机号验证
class MobileCountView(APIView):
    '''
    手机号验证
    '''
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data)


class UserView(CreateAPIView):
    '''
    用户注册
    '''
    serializer_class = CreateUserSerializer