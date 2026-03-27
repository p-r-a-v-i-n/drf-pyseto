from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .conf import get_settings
from .serializers import TokenObtainPairSerializer, TokenRefreshSerializer


class TokenObtainPairView(APIView):
    permission_classes = []
    authentication_classes = []

    def get_authenticate_header(self, request):
        return get_settings().auth_header_type

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    permission_classes = []
    authentication_classes = []

    def get_authenticate_header(self, request):
        return get_settings().auth_header_type

    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
