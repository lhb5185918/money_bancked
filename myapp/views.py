from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User, Account
from .serializers import UserSerializer, LoginSerializer, AccountSerializer

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return Response({
                'code': 200,
                'message': 'token刷新成功',
                'data': {
                    'access': response.data['access']
                }
            })
        except Exception as e:
            return Response({
                'code': 400,
                'message': 'token刷新失败',
                'errors': {
                    'refresh': ['请提供有效的refresh token']
                }
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create(
            username=request.data['username'],
            password=request.data['password'],  # 注意：实际应用中应该加密密码
            nick_name=request.data.get('nick_name', ''),
            description=request.data.get('description', '')
        )
        return Response({
            'code': 200,
            'message': '注册成功',
            'data': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'code': 400,
        'message': '参数错误',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(username=username)
            if user.password == password:  # 注意：实际应用中应该使用加密密码
                # 生成token
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'code': 200,
                    'message': '登录成功',
                    'data': {
                        'token': f"Bearer {str(refresh.access_token)}",
                        'refresh_token': str(refresh),
                        'user': UserSerializer(user).data
                    }
                })
            else:
                return Response({
                    'code': 400,
                    'message': '密码错误'
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'code': 400,
                'message': '用户不存在'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'code': 400,
        'message': '参数错误',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def account_list(request):
    try:
        # 验证用户信息
        if not request.user.is_authenticated:
            return Response({
                'code': 401,
                'message': '认证失败',
                'errors': {
                    'detail': '用户未登录'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == 'POST':
            # 创建新账户
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                return Response({
                    'code': 200,
                    'message': '创建账户成功',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'code': 400,
                'message': '参数错误',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'GET':
            # 获取所有账户
            accounts = Account.objects.all()
            serializer = AccountSerializer(accounts, many=True)
            return Response({
                'code': 200,
                'message': '获取账户列表成功',
                'data': serializer.data
            })
    except Exception as e:
        return Response({
            'code': 500,
            'message': '服务器内部错误',
            'errors': {
                'detail': str(e)
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
