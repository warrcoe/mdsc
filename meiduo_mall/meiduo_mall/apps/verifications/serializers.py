from django_redis import get_redis_connection
from redis import RedisError
from rest_framework import serializers


class ImageCodeCheckSerializer(serializers.Serializer):
    '''
    图片验证码校验序列化器
    '''
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        '''
        校验
        '''
        image_code_id = attrs['image_code_id']
        text = attrs['text']
        # 查询真实图片验证码
        redis_conn = get_redis_connection('verify_codes')
        real_image_code_text = redis_conn.get('img_%s' % image_code_id)
        # 校验图片验证码
        if not real_image_code_text:
            raise serializers.ValidationError('图片验证码无效')
        # 删除图片验证码
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            from meiduo_mall.utils.exceptions import logger
            logger.error(e)
        # 对比图片验证码
        real_image_code_text = real_image_code_text.decode()
        if text.lower() != real_image_code_text.lower():
            raise serializers.ValidationError('图片验证码错误')
        # 判断是否在60s内
        mobile = self.context['view'].kwargs['mobile']
        send_flag = redis_conn.get('send_flag_' + mobile)
        if send_flag:
            raise serializers.ValidationError('请求次数过于频繁')

        return attrs



