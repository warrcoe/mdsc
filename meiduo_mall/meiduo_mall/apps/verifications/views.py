import random

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

from apps.verifications import serializers
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection

from libs.yuntongxun.sms import CCP
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


class SMSCodeView(GenericAPIView): #GenericAPIView校验参数棒棒的！
        '''短信验证码
        1、接收参数
        2、校验参数（通过serializer来教研）
        3、业务处理
        4、返回结果
        '''
        serializer_class = serializers.ImageCodeCheckSerializer

        # 1、接收参数 mobile image_code_id text
        def get(self, request, mobile):
            # 判断图片验证码，短信验证码是否在60s内
            serializer = self.get_serializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)

        # 2、校验参数
            # 生成短信验证码
            sms_code = '%06d' % random.randint(0, 999999)
            print(sms_code)
            # 生成管道
            redis_conn = get_redis_connection('verify_codes')
            pl = redis_conn.pipeline()
            pl.setex('sms_' + mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
            pl.setex('send_flag_' + mobile,constants.SEND_SMS_CODE_INTERVAL,1)
            pl.execute()
        # 3、业务处理
            # 发送短信
            ccp = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES//60], constants.SMS_CODE_TEMP_ID)
        # 4、返回结果
            return Response({'message' : 'OK'})



