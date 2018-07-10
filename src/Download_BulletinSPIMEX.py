# -*- coding: utf-8 -*-

""" Download all SPIMEX bulletin
@created July 6, 2018
@author: Ilya Zlotnik

The script downloads historical market data for the Derivatives Market of 
St. Petersburg International Mercantile Exchange (SPIMEX), see 
http://spimex.com/en/derivatives/market-portrait/ for details. 
This script automates downloading of so-called daily bulletins,
which can be downloaded by hand for free from 
http://spimex.com/en/derivatives/trades/results/
Please, be aware that on non business day (for example, Russian holidays) 
there is no trades and no market data is available.

Note:
  Set start_date and end_date to appropriate values. For example, setting
    start_date = datetime.datetime(2017, 8, 18)
    end_date = datetime.datetime(2018, 7, 6)
  the script will download all available data from August 18, 2017 to July 6, 2018.
  
  To download all available data use 
    start_date = datetime.datetime(2010, 12, 17)
    end_date = datetime.datetime.today()
  As of July 6, 2018 the execution time with the parameters above 
  can be about 20 minutes to download all the data (762 files).
"""

import datetime
import os
from urllib.request import urlopen
from urllib.error import HTTPError


if __name__ == '__main__':
    print('* START *')

    # Set the download period [start_date, end_date]
    start_date = datetime.datetime(2018, 7, 8)
    end_date = datetime.datetime.today()

    # Set the target path
    target_path = '../data/source'

    # Create the target path if it has not been created yet
    if not os.path.exists(target_path):
        print('Create file path %s' % target_path)
        os.makedirs(target_path)

    # Market runs since December 17, 2010
    min_start_date = datetime.datetime(2010, 12, 17)
    if start_date < min_start_date:
        start_date = min_start_date

    # There is no data for future trade dates
    max_end_date = datetime.datetime.today()
    if end_date > max_end_date:
        end_date = max_end_date

    # STEP 1. Download data from December 17, 2010 to June 1, 2015
    # combined in one single file, see 
    # http://spimex.com/files/6488/fut_xls_20101217_20150601.xls
    current_date = datetime.datetime(2015, 6, 1)
    if start_date == min_start_date and current_date <= end_date:
        filename = 'fut_xls_' + start_date.strftime('%Y%m%d') + '_' + current_date.strftime('%Y%m%d') + '.xls'
        url = 'http://spimex.com/files/6488/'

        # Attempt to download the file
        body = ''
        try:
            body = urlopen(url).read()
        except HTTPError:
            pass

        # Save the file if it was successfully downloaded
        if body:
            with open(os.path.join(target_path, filename), 'wb') as fh_filename:
                fh_filename.write(body)
            print("Date from/till=%s/%s, URL=%s %s" % (start_date.strftime('%Y%m%d'),
                                                       current_date.strftime('%Y%m%d'),
                                                       url, filename))
        else:
            print("[SKIP] Date from/till=%s/%s URL=%s" % (start_date.strftime('%Y%m%d'),
                                                          current_date.strftime('%Y%m%d'),
                                                          url))
        # Update the current date
        start_date = current_date + datetime.timedelta(days=1)

    # STEP 2. Download data from current_date (after June 1, 2015)
    # to end_date (less than today), see for example
    # http://spimex.com/upload/reports_fte/fut_xls/fut_xls_20180712170000.xls
    # For each day between start_date and end_date run the script
    current_date = start_date
    while current_date <= end_date:
        filename = 'fut_xls_' + current_date.strftime('%Y%m%d') + '170000.xls'
        url = 'http://spimex.com/upload/reports_fte/fut_xls/' + filename

        # Try to get the file
        body = ''
        try:
            body = urlopen(url).read()
        except HTTPError:
            pass

        # Save the file if it was successfully downloaded
        if body:
            with open(os.path.join(target_path, filename), 'wb') as fh_filename:
                fh_filename.write(body)
            print("Date=%s URL=%s %s" % (current_date.strftime('%Y%m%d'), url, filename))
        else:
            print("[SKIP] Date=%s URL=%s" % (current_date.strftime('%Y%m%d'), url))

        # Next iteration
        current_date = current_date + datetime.timedelta(days=1)
    
    print('* STOP  *')
