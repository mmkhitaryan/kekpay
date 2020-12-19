from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateChallengeSerializer


class ObtainChallengeJWT(APIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = CreateChallengeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data
        )
