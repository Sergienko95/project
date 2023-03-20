from datetime import datetime

import pendulum


def utcnow() -> datetime:
    return pendulum.now().in_tz("UTC")
