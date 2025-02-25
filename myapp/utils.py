from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

def custom_user_authentication_rule(user):
    """
    自定义用户认证规则
    """
    return True if user is not None else False

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        error_detail = str(response.data.get('detail', '未知错误'))
        
        # 处理JWT相关错误
        if isinstance(exc, (InvalidToken, TokenError)):
            return Response({
                'code': response.status_code,
                'message': '认证失败',
                'errors': {
                    'detail': '无效的token或token已过期，请重新登录'
                }
            }, status=response.status_code)
            
        # 处理认证相关错误
        if response.status_code == 401:
            return Response({
                'code': 401,
                'message': '认证失败',
                'errors': {
                    'detail': '请先登录或提供有效的认证信息'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response({
            'code': response.status_code,
            'message': '请求失败',
            'errors': {
                'detail': error_detail
            }
        }, status=response.status_code)
    
    return Response({
        'code': 500,
        'message': '服务器内部错误',
        'errors': {
            'detail': str(exc)
        }
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 