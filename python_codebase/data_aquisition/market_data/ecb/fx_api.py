import requests
import datetime
import pandasdmx as sdmx


def get_ecb_data_api(start_date: datetime.date = datetime.date.today(), end_date: datetime.date = datetime.date.today()):
    ecb = sdmx.Request("ECB")
    parameters = {
        "startPeriod": f"{start_date:%Y-%m-%d}",
        "endPeriod": f"{end_date:%Y-%m-%d}",
    }
    data_response = ecb.data(
        resource_id="EXR",
        key={"CURRENCY": ["CHF", "USD", "GBP", "AUD"]},
        params=parameters,
    )
    data = data_response.to_pandas()
    return data
