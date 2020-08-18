from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from utils.jwt_token.jwt_auth import create_token
from .models import User

# Create your views here.


class LoginCheck(APIView):

    # 通过Authorization请求头传递token
    # authentication_classes = [JwtAuthorizationMiddleware, ]
    def get(self, request):
        # user = User.objects.filter()
        print('get方法成功')
        return JsonResponse(
            {
                'code': 'get success',
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        try:
            req = request.data
            print(req)
            req_username = req['username']
            req_password = req['password']
            user = User.objects.get(username=req_username)
            if user.password == req_password:
                token = create_token(
                    {
                        'username': req_username,
                        'password': req_password
                    }
                )
                return JsonResponse(
                    {
                        "code": "登陆成功",
                        'token': token
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return JsonResponse(
                    {
                        'code': '登录失败'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    'code': '登录失败'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

    def put(self, request):
        try:
            person = User()
            person.username = request.data.get('username')
            person.password = request.data.get('password')
            person.email = request.data.get('email')
            person.telephone = request.data.get('telephone')
            person.sex = request.data.get('sex')
            # print(person.username, person.password, person.email, person.telephone, person.sex)
            person.save()
            return JsonResponse(
                {
                    'code': '添加成功'
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    'code': '添加失败'
                }
            )


# addUser('admin',123456,13260666950,'male')
