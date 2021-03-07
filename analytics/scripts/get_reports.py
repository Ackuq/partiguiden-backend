import os

from standpoints.models import Subject
from standpoints.serializer import SubjectSerializer

CATEGORY_VIEW_ID = os.environ.get("ANALYTICS_CATEGORY_VIEW_ID", "0")


def format_report(report):
    data = []

    for row in report["data"]["rows"]:
        subject_id = row["dimensions"][0].replace("/standpoints/", "")
        value = row["metrics"][0]["values"][0]
        if subject_id.isdigit():
            subject_id = int(subject_id, base=10)
            try:
                subject = Subject.objects.get(pk=subject_id)
                serialized = SubjectSerializer(subject)
                data.append((serialized.data, value))
            except Subject.DoesNotExist:
                pass  # Don't do anything

    return data


def get_reports(analytics):
    reports = (
        analytics.reports()
        .batchGet(
            body={
                "reportRequests": [
                    {
                        "viewId": CATEGORY_VIEW_ID,
                        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
                        "metrics": [
                            {"expression": "ga:pageviews"},
                        ],
                        "dimensions": [{"name": "ga:pagePath"}],
                        "dimensionFilterClauses": [
                            {
                                "filters": [
                                    {
                                        "dimensionName": "ga:pagePath",
                                        "operator": "REGEXP",
                                        "expressions": ["standpoints/.+"],
                                    }
                                ]
                            }
                        ],
                    }
                ]
            }
        )
        .execute()
    )
    return format_report(reports["reports"][0])
