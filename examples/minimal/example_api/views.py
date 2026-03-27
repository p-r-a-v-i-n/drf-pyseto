from rest_framework.response import Response
from rest_framework.views import APIView


class WhoAmIView(APIView):
    def get(self, request):
        return Response(
            {
                "user_id": getattr(request.user, "id", None),
                "username": getattr(request.user, "username", None),
                "is_authenticated": request.user.is_authenticated,
            }
        )
