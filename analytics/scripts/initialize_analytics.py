import json
import os

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

SERVICE_ACCOUNT = json.loads(os.environ.get("ANALYTICS_SERVICE_ACCOUNT", ""))


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(SERVICE_ACCOUNT, SCOPES)

    # Build the service object.
    analytics = discovery.build("analyticsreporting", "v4", credentials=credentials)

    return analytics
