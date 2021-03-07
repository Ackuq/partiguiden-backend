import json
import os

from google.analytics.data_v1alpha import AlphaAnalyticsDataClient

SERVICE_ACCOUNT = json.loads(os.environ.get("ANALYTICS_SERVICE_ACCOUNT", ""))


def initialize_analytics():
    client = AlphaAnalyticsDataClient.from_service_account_info(SERVICE_ACCOUNT)
    return client
