from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants
# Create your views here.


class ImageCodeView(APIView):
    '''提供图片验证码'''
    def get(self, request, image_code_id):
        # 获取图片验证码信息
        text, image = captcha.generate_captcha()
        # 保存信息到redis数据库
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex('img_' + image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        # 返回验证码图片本身
        return HttpResponse(image, content_type='images/jpg')


