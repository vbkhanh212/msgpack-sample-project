from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .MessagePackParser import MessagePackParser
from .MessagePackRenderer import MessagePackRenderer

class DataView(APIView):
    """
    This endpoint accepts data and echoes a response.
    It supports both JSON and MessagePack based on headers.
    """
    parser_classes = [MessagePackParser, JSONParser] 
    renderer_classes = [MessagePackRenderer, JSONRenderer]

    def post(self, request):
        name = request.data.get('name', 'Guest')
        age = request.data.get('age', 0)
        description = request.data.get('description', '')
        
        response_data = {
            'name': name,
            'age': age,
            'description': description
        }

        return Response(response_data, status=status.HTTP_200_OK)
    