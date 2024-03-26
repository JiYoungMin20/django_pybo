from .base import *

# 서비스용 AWS 고정 IP 주소
ALLOWED_HOSTS = ['43.200.48.35']
# css, js, image 파일등 static 디렉토리 위치 지정
STATIC_ROOT = BASE_DIR / 'static/'
# STATIC_ROOT = BASE_DIR / 'pybo/static/'
STATICFILES_DIRS = []
# DEBUG를 False로 설정하기
DEBUG = False 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pybo',
        'USER': 'dbmasteruser',
        'PASSWORD': '}.nER7DQK?l:RYGT~5ha;4Jq,As?-Cwh',
        'HOST': 'ls-d2b48d1fbffd300a1820eb8add1208caf309a059.c7wiak6ag4yg.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}