from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response

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
