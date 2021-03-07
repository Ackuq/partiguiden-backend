import os

from google.analytics.data_v1alpha import AlphaAnalyticsDataClient
from google.analytics.data_v1alpha.types import Dimension, Metric, RunReportRequest, Entity, DateRange
from standpoints.models import Subject
from standpoints.serializer import SubjectSerializer

ANALYTICS_PROPERTY = os.environ.get("ANALYTICS_PROPERTY", "0")


def format_report(report):
    data = []

    for row in report["data"]["rows"]:
        subject_id = row["dimensions"][0].replace("/standpoints/", "")
        value = row["metrics"][0]["values"][0]
        if subject_id.isdigit() and value.isdigit():
            subject_id = int(subject_id, base=10)
            value = int(value, 10)
            try:
                subject = Subject.objects.get(pk=subject_id)
                serialized = SubjectSerializer(subject)
                data.append((serialized.data, value))
            except Subject.DoesNotExist:
                pass  # Don't do anything

    return data


def get_reports(client: AlphaAnalyticsDataClient):
    request = RunReportRequest(
        entity=Entity(property_id=ANALYTICS_PROPERTY),
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    )

    # reports = (
    #     analytics.reports()
    #     .batchGet(
    #         body={
    #             "reportRequests": [
    #                 {
    #                     "viewId": CATEGORY_VIEW_ID,
    #                     "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    #                     "metrics": [
    #                         {"expression": "ga:pageviews"},
    #                     ],
    #                     "dimensions": [{"name": "ga:pagePath"}],
    #                     "dimensionFilterClauses": [
    #                         {
    #                             "filters": [
    #                                 {
    #                                     "dimensionName": "ga:pagePath",
    #                                     "operator": "REGEXP",
    #                                     "expressions": ["standpoints/.+"],
    #                                 }
    #                             ]
    #                         }
    #                     ],
    #                 }
    #             ]
    #         }
    #     )
    #     .execute()
    # )
    response = client.run_report(request)
    for row in response.rows:
        print(row)
    return response.rows
