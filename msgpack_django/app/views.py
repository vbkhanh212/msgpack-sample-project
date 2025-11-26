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
            'message': f"Hello, {name}! We received your request",
            'age': age,
            'description': description,
            'data_format': request.accepted_renderer.media_type
        }

        # DRF's Response object will be serialized by the chosen renderer
        return Response(response_data, status=status.HTTP_200_OK)
    