from .base import *

# 서비스용 AWS 고정 IP 주소
ALLOWED_HOSTS = ['43.200.48.35']
# css, js, image 파일등 static 디렉토리 위치 지정
# STATIC_ROOT = BASE_DIR / 'static/'
STATIC_ROOT = BASE_DIR / 'pybo/static/'
STATICFILES_DIRS = []
# DEBUG를 False로 설정하기
DEBUG = False 