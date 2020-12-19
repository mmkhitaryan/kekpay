from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CreateChallengeSerializer, AttemntChallengeSerializer

class BaseChallenges(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data
        )

class ObtainChallengeJWT(BaseChallenges):
    serializer_class = CreateChallengeSerializer

class AttemptChallenge(BaseChallenges):
    serializer_class = AttemntChallengeSerializer
