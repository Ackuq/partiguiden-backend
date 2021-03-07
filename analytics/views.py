from analytics.scripts.get_reports import get_reports
from analytics.scripts.initialize_analytics import initialize_analyticsreporting
from rest_framework.views import APIView
from rest_framework.response import Response


analytics = initialize_analyticsreporting()


class PopularView(APIView):
    def get(self, request):
        reports = get_reports(analytics)
        return Response(reports)
