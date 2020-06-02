import pandas as pd
CANADA_RAWCASES_URL = \
        "https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/timeseries_hr/cases_timeseries_hr.csv"


def stage_latest() -> pd.DataFrame:
    canada_raw = pd.read_csv(CANADA_RAWCASES_URL)
    canada_raw['Combined_Key'] = canada_raw.apply(
        lambda x: str(x['province']) + ', ' + str(x['health_region']) + ', ' + 'CA', axis=1)
    canada_raw.drop(columns=['province', 'health_region', 'cumulative_cases'], inplace=True)
    canada_raw = canada_raw.pivot(index='Combined_Key', columns='date_report', values='cases')
    return canada_raw
