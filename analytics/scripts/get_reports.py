import os
from typing import List, Tuple

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    Metric,
    OrderBy,
    RunReportRequest,
    RunReportResponse,
)
from rest_framework.utils.serializer_helpers import ReturnDict

from standpoints.models import Subject
from standpoints.serializer import SubjectListSerializer

ANALYTICS_PROPERTY = os.environ.get("ANALYTICS_PROPERTY", "0")


def format_popular(report: RunReportResponse) -> List[Tuple[ReturnDict, int]]:
    data = []

    for row in report.rows:
        subject_id = row.dimension_values[0].value.replace("/standpoints/", "")
        value = row.metric_values[0].value
        if subject_id.isdigit() and value.isdigit():
            subject_id = int(subject_id, base=10)
            value = int(value, 10)
            try:
                subject = Subject.objects.get(pk=subject_id)
                serialized = SubjectListSerializer(subject)
                data.append((serialized.data, value))
            except Subject.DoesNotExist:
                pass  # Don't do anything

    return data


def get_popular_standpoints(client: BetaAnalyticsDataClient) -> List[Tuple[ReturnDict, int]]:
    request = RunReportRequest(
        property="properties/{}".format(ANALYTICS_PROPERTY),
        dimensions=[Dimension(name="pagePathPlusQueryString")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="pagePathPlusQueryString",
                string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType(6), value="standpoints/.+"),
            )
        ),
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
        limit=10,
    )

    response = client.run_report(request)
    data = format_popular(response)

    return data
