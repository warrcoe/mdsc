from celery import Celery
# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 创建celery应用
celery_app = Celery('meiduo')
# 导入celery配置
celery_app.config_from_object('celery_tasks.config')
# 自动将异步任务注册到celery_app
# 提示：不需要指向tasks.py;因为celery默认回去寻找tasks.py同名的文件
celery_app.autodiscover_tasks(['celery_tasks.sms'])

# 开启celery的worker
# celery -A celery实例应用包路径 worker -l info
# celery -A celery_tasks.main worker -l info

# windows10环境下用一下命令启动celery服务
# celery -A celery_tasks.main worker -l info -P eventlet