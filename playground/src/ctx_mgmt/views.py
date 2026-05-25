from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response


class HelloWorldView(APIView):
    def post(self, request):
        return Response({"message": "Hello World"}, status=HTTP_200_OK)
