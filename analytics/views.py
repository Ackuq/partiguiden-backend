from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.scripts.get_reports import get_reports
from analytics.scripts.initialize_analytics import initialize_analytics

client = initialize_analytics()


class PopularView(APIView):
    def get(self, request):
        reports = get_reports(client)
        return Response(reports)
