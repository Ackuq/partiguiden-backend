import json
import os
from typing import Optional

from google.analytics.data_v1beta import BetaAnalyticsDataClient

SERVICE_ACCOUNT_JSON = os.environ.get("ANALYTICS_SERVICE_ACCOUNT", None)

if SERVICE_ACCOUNT_JSON is None:
    ANALYTICS_FILE = os.environ.get("ANALYTICS_SERVICE_ACCOUNT_FILE", None)
    if ANALYTICS_FILE is not None:
        analytics_file = open(ANALYTICS_FILE, "r")
        SERVICE_ACCOUNT_JSON = analytics_file.read()


def initialize_analytics() -> Optional[BetaAnalyticsDataClient]:
    if SERVICE_ACCOUNT_JSON is not None:
        client: BetaAnalyticsDataClient = BetaAnalyticsDataClient.from_service_account_info(
            json.loads(SERVICE_ACCOUNT_JSON)
        )
        return client
    return None
