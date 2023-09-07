from datetime import date, datetime

import legacy.util_gsb as util_gsb
import pandas as pd
from chase_redirect import REDIRECT_CHAIN_CSV_PATH
import numpy as np


def get_rows_to_check(df):

    if 'Blacklisted' not in df:
        return df

    return df.loc[df['Blacklisted'] != 1]


def do_query(url_lst):
    count = 0
    phishing, mal = [], []
    while count < len(url_lst):

        if count + 400 > len(url_lst):
            p_tmp, m_tmp = util_gsb.check_urls(url_lst[count:])
        else:
            p_tmp, m_tmp = util_gsb.check_urls(url_lst[count: count + 400])
        phishing += p_tmp
        mal += m_tmp
        count += 500

    # phishing, mal = util_gsb.check_urls(url_lst)
    bad_guys = set(phishing + mal)

    return bad_guys


def query_gsb_and_update(csv_file=REDIRECT_CHAIN_CSV_PATH):

    df = pd.read_csv(csv_file, low_memory=False)

    if 'Blacklisted' not in df:
        df['Blacklisted'] = np.nan
    if 'BL_date' not in df:
        df['BL_date'] = np.nan

    check_list = get_rows_to_check(df)
    url_lst = check_list['url'].to_list()

    bad_guys = do_query(url_lst)

    for index, row in get_rows_to_check(df).iterrows():

        if row['url'] in bad_guys:
            df.at[index, 'Blacklisted'] = 1
            df.at[index, 'BL_date'] = datetime.now().timestamp()

    df.to_csv('./redirection_bl.csv', index=False)


def run():
    query_gsb_and_update()


if __name__ == '__main__':
    
    import schedule
    import time
    
    # run()
    # schedule.every().day.at("10:20").do(run)
    schedule.every().hour.do(run)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    run()
