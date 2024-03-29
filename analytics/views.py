from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.scripts.get_reports import get_popular_standpoints
from analytics.scripts.initialize_analytics import initialize_analytics

client = initialize_analytics()


class PopularView(APIView):
    def get(self, request: Request) -> Response:
        if client is None:
            return Response()
        reports = get_popular_standpoints(client)
        return Response(reports)
