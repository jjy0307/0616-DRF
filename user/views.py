from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate, logout
from user.serializers import CustomUserSerializer
from user.models import CustomUser as CustomUserModel


class UserView(APIView):
    def get(self, request):
        user = request.user
        return Response(CustomUserSerializer(user).data)

    def post(self, request):
        # serializer의 data 인자에는 model로 지정 된 테이블의 field:value를 dictionary로 넘겨준다.
        user_serializer = CustomUserSerializer(data=request.data)
        # serializer validator를 통과하지 않을 경우 .is_valid()가 False로 return된다.
        if user_serializer.is_valid():
            # validator를 통과했을 경우 데이터 저장
            user_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)

        # .errors에는 validator에 실패한 필드와 실패 사유가 담겨져 있다.
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        # 원래 request.user로 받는게 맞음
        user = CustomUserModel.objects.get(id=obj_id)
        user_serializer = CustomUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=200)

        return Response(user_serializer.errors, status=400)


class UserApiView(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)

    def delete(self, request):
        logout(request)
        return Response({'message': '로그아웃 성공!'})