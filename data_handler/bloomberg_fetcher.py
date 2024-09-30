import logging
import os

import blpapi
import pandas as pd
import pdblp
from src.utilities.date_time import dates_manipulation as dtm

logger = logging.getLogger(__name__)


def bbg_apply(function, ticker_list: list, field_list: list,
              startDate: str = None, endDate: str = None,
              periodicityAdjustment: str = None,
              periodicitySelection: str = None, maxDataPoints: int = None):
    """
    Supported functions:
    BDP, BDP_drillingIntoIndividualElements, BDS, BDH, BEQS
    """
    session = blpapi.Session()
    if not session.start():
        print("Failed to start bloomberg session.")
    if not session.openService("//blp/refdata"):
        print("Failed to open bloomberg service.")
    service = session.getService("//blp/refdata")
    if ('BDP' in function.__name__) or ('BDS' in function.__name__):
        request = service.createRequest("ReferenceDataRequest")
        x = function(session, request, ticker_list, field_list)
    elif 'BDH' in function.__name__:
        request = service.createRequest("HistoricalDataRequest")
        x = function(session, request, ticker_list, field_list, startDate, endDate, periodicityAdjustment,
                     periodicitySelection, maxDataPoints)
    elif 'BEQS' in function.__name__:
        request = service.createRequest("BeqsRequest")
    return x


def set_trading_dates(start_date: str, end_date: str):
    return pd.date_range(start_date, end_date, freq='BM')


def BEQS(screen_name: str, as_of_date: str, screen_type: str = 'PRIVATE'):
    session = blpapi.Session()
    session.start()
    session.openService("//blp/refdata")
    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("BeqsRequest")
    request.set("screenName", screen_name)
    request.set("screenType", screen_type)
    overrides = request.getElement("overrides")
    override1 = overrides.appendElement()
    override1.setElement("fieldId", "PiTDate")
    override1.setElement("value", as_of_date)
    session.sendRequest(request)
    endReached = False
    ticker_list = []
    while endReached == False:
        blpEvent = session.nextEvent()
        if blpEvent.eventType() == blpapi.Event.RESPONSE or blpEvent.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            for message in blpEvent:
                for j in range(message.getElement('data').getElement('securityData').numValues()):
                    ticker_list.append(message.getElement('data').getElement('securityData').getValue(j).getElement(
                        'security').getValue())
        if blpEvent.eventType() == blpapi.Event.RESPONSE:
            endReached = True
    ticker_list = [s + ' Equity' for s in ticker_list]
    return ticker_list


def get_all_tickers_over_history_for_screen(screen_name: str, start_date: str, end_date: str) -> list:
    s_date_as_hyphen_string = dtm.set_hyphenated_string_date(start_date)
    s_date_as_date = dtm.stringToDate(s_date_as_hyphen_string)
    e_date_as_hyphen_string = dtm.set_hyphenated_string_date(end_date)
    e_date_as_date = dtm.stringToDate(e_date_as_hyphen_string)
    as_of_date_no_hyphen = start_date
    temp_ticker_list = []
    while s_date_as_date < e_date_as_date:
        temp_ticker_list.extend(BEQS(screen_name, as_of_date_no_hyphen, screen_type='PRIVATE'))
        s_date_as_hyphen_string = dtm.pushDate_forward(s_date_as_hyphen_string, months=1)
        as_of_date_no_hyphen = dtm.set_unhyphenated_string_date(s_date_as_hyphen_string)
        s_date_as_date = dtm.stringToDate(s_date_as_hyphen_string)
        print(s_date_as_hyphen_string, len(temp_ticker_list))
    ticker_list = list(set(temp_ticker_list))
    ticker_list.sort()
    return ticker_list


def get_all_tickers_over_history_for_screen_as_dataframe(screen_name: str,
                                                         trading_dates) -> pd.DataFrame:
    df_tickers = pd.DataFrame(index=trading_dates, columns=['tickers'])
    for j in trading_dates:
        date_no_hyphen = dtm.set_unhyphenated_string_date(dtm.dateToString(j))
        df_tickers.loc[j, 'tickers'] = BEQS(screen_name, date_no_hyphen, screen_type='PRIVATE')
        print(date_no_hyphen, df_tickers.loc[j])
    return df_tickers


def get_all_tickers_over_history_for_screen_as_dict(screen_name: str, df_for_dates: pd.DataFrame) -> dict:
    ticker_dict = {}
    for j in df_for_dates.index:
        unhyphenated_string_date = dtm.set_unhyphenated_string_date(dtm.dateToString(j))
        ticker_dict[j] = BEQS(screen_name, unhyphenated_string_date, screen_type='PRIVATE')
    return ticker_dict


def get_financial_ratio_between_history(ticker_list: list,
                                        start_date: str,
                                        end_date: str,
                                        financial_ratio: str,
                                        periodicity_selection_string: str = 'DAILY') -> pd.DataFrame:
    con = pdblp.BCon(debug=False)
    con.start()
    df = con.bdh(ticker_list, financial_ratio, start_date, end_date,
                 elms=[('periodicitySelection', periodicity_selection_string)])
    df.columns = df.columns.droplevel(level=1)  # remove fields
    del df.index.name
    del df.columns.name
    return df


def get_data_for_screen(screen_name: str, start_date: str, end_date: str, financial_ratio: str = 'PX_LAST'):
    ticker_list = get_all_tickers_over_history_for_screen(screen_name, start_date, end_date)
    df = get_financial_ratio_between_history(ticker_list, start_date, end_date, financial_ratio,
                                             periodicity_selection_string='DAILY')
    return df


def write_data(data_to_write, path_results, name_of_data_to_write):
    filepath_and_name = os.path.join(path_results, name_of_data_to_write + '.csv')
    data_to_write.to_csv(filepath_and_name, encoding='utf-8')
    return None


def write_financial_ratio_between_history(ticker_list: list,
                                          start_date: str,
                                          end_date: str,
                                          financial_ratio: str,
                                          path_results: str,
                                          name_of_data_to_write: str,
                                          periodicity_selection_string: str = 'DAILY'):
    df = get_financial_ratio_between_history(ticker_list, start_date, end_date, financial_ratio,
                                             periodicity_selection_string)
    write_data(df, path_results, name_of_data_to_write)
    return None


def set_message_to_dict_of_dataframes(message, ticker_list: list, field_list: list) -> dict:
    """
    Input:
    1. Bloomberg response message
    2. ticker_list: a list of tickers
    3. field_list: a list of fields
    OUTPUT:
    1. Dictionary of dataframes
    Each key in the dictionary corresponds to a field.
    The value corresponding to the key is a dataframe, where the columns are the tickers,
    rows are the dates (in the case of BDH requests) and the values are fields corresponding
    to the tickers on a given date.
    """
    dict_of_df = {}
    for field in field_list:
        dict_of_df[field] = pd.Series()
        for ticker in range(len(ticker_list)):
            dict_of_df[field].set_value(ticker_list[ticker],
                                        message.getElement("securityData").getValue(ticker).getElement(
                                            "fieldData").getElement(field).getValue())
    return dict_of_df


def BDP(session, request, ticker_list: list, field_list: list):
    for ticker in ticker_list:
        request.append("securities", ticker)
    for field in field_list:
        request.append("fields", field)
    session.sendRequest(request)
    endReached = False
    while endReached == False:
        blpEvent = session.nextEvent()
        if blpEvent.eventType() == blpapi.Event.RESPONSE or blpEvent.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            for message in blpEvent:
                print(message)
        if blpEvent.eventType() == blpapi.Event.RESPONSE:
            endReached = True
    return message


def BDP_drillingIntoIndividualElements(session, request, ticker_list: list, field_list: list):
    for ticker in ticker_list:
        request.append("securities", ticker)
    for field in field_list:
        request.append("fields", field)
    session.sendRequest(request)
    endReached = False
    while endReached == False:
        blpEvent = session.nextEvent()
        if blpEvent.eventType() == blpapi.Event.RESPONSE or blpEvent.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            for message in blpEvent:
                for ticker in range(len(ticker_list)):
                    for field in field_list:
                        print(ticker_list[ticker], ":", field, "= ")
                        try:
                            print(
                                message.getElement("securityData").getValue(ticker).getElement("fieldData").getElement(
                                    field).getValue())
                        except blpapi.exception.NotFoundException:
                            print('NOT FOUND')
        if blpEvent.eventType() == blpapi.Event.RESPONSE:
            endReached = True
    return message


def BDS(session, request, ticker_list: list, field_list: list):
    for ticker in ticker_list:
        request.append("securities", ticker)
    for field in field_list:
        request.append("fields", field)
    session.sendRequest(request)
    endReached = False
    while endReached == False:
        blpEvent = session.nextEvent()
        if blpEvent.eventType() == blpapi.Event.RESPONSE or blpEvent.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            for message in blpEvent:
                print(message)
        if blpEvent.eventType() == blpapi.Event.RESPONSE:
            endReached = True
    return message


def BDH(session, request, ticker_list: list,
        field_list: list, startDate: str, endDate: str, periodicityAdjustment: str = 'ACTUAL',
        periodicitySelection: str = 'MONTHLY', maxDataPoints: int = 100):
    for ticker in ticker_list:
        request.append("securities", ticker)
    for field in field_list:
        request.append("fields", field)
    request.set("periodicityAdjustment", periodicityAdjustment)
    request.set("periodicitySelection", periodicitySelection)
    request.set("startDate", startDate)
    request.set("endDate", endDate)
    request.set("maxDataPoints", maxDataPoints)
    session.sendRequest(request)
    endReached = False
    while endReached == False:
        blpEvent = session.nextEvent()
        if blpEvent.eventType() == blpapi.Event.RESPONSE or blpEvent.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            for message in blpEvent:
                print(message)
        if blpEvent.eventType() == blpapi.Event.RESPONSE:
            endReached = True
    return message


def BDP_with_overrrides(session, request):
    request.append("securities", "IBM US Equity")
    request.append("fields", "INTERVAL_HIGH")
    # add overrides
    # override 1
    overrides = request.getElement("overrides")
    override1 = overrides.appendElement()
    override1.setElement("fieldId", "END_DATE_OVERRIDE")
    override1.setElement("value", "20150101")
    # override 2
    override2 = overrides.appendElement()
    override2.setElement("fieldId", "CALC_INTERVAL")
    override2.setElement("value", "2Y")
    print(request)
    session.sendRequest(request)
    endReached = False
    while endReached == False:
        blpEvent = session.nextEvent()
        if blpEvent.eventType() == blpapi.Event.RESPONSE or blpEvent.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            for message in blpEvent:
                print(message)
        if blpEvent.eventType() == blpapi.Event.RESPONSE:
            endReached = True
    return None


def BDS_with_overrides(session, request):
    request.append("securities", "YCGT0025 Index")
    request.append("fields", "CURVE_TENOR_RATES")
    overrides = request.getElement("overrides")
    override1 = overrides.appendElement()
    override1.setElement("fieldId", "CURVE_DATE")
    override1.setElement("value", "20150101")
    session.sendRequest(request)
    endReached = False
    while endReached == False:
        blpEvent = session.nextEvent()
        if blpEvent.eventType() == blpapi.Event.RESPONSE or blpEvent.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            for message in blpEvent:
                print(message)
        if blpEvent.eventType() == blpapi.Event.RESPONSE:
            endReached = True
    return None


def bbg_BDH_withElementsAndValues(session, request):
    request.getElement("securities").appendValue("IBM US Equity")
    request.getElement("fields").appendValue("PX_LAST")
    request.set("periodicityAdjustment", "ACTUAL")
    request.set("periodicitySelection", "MONTHLY")
    request.set("startDate", "20100101")
    request.set("endDate", "20141231")
    request.set("maxDataPoints", 100)
    session.sendRequest(request)
    endReached = False
    while endReached == False:
        blpEvent = session.nextEvent()
        if blpEvent.eventType() == blpapi.Event.RESPONSE or blpEvent.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            for message in blpEvent:
                fieldData = message.getElement("securityData").getElement("fieldData")
                for i in range(fieldData.numValues()):
                    dt = fieldData.getValueAsElement(i).getElement("date").getValue()
                    px = fieldData.getValueAsElement(i).getElement("PX_LAST").getValue()
                    print(dt, px)
        if blpEvent.eventType() == blpapi.Event.RESPONSE:
            endReached = True
    return None
