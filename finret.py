import numpy as np
import scipy as sp
import pandas as p
import urllib
import json
import socket
import os
import time
import sys
from datetime import *
from scipy.stats import norm
from scipy.stats import multivariate_normal
from scipy.stats import chi2
from scipy.stats import laplace
from scipy.stats import percentileofscore
from random import randint


class fred_api:

    
    ##Initialize with FRED Key and series ID(s)##
    def __init__(self, fred_key, series_id):

        
        ##Unique FRED Access Key
        self.FRED_API_Key = fred_key
        self.series_id = series_id 

        ##Check that the 'series_id' arguement is a list. If so, then determine
        ##which series has the largest time period intervals.
        if type(self.series_id) == list:
            
            self.time_type = 4
            
            for x in self.series_id:
                self.file_type = 'json'
                self.url = ('https://api.stlouisfed.org/fred/series?series_id='
                            + x + '&api_key=' + self.FRED_API_Key
                            + '&file_type=' + self.file_type)
                           
                ##Get the Data   
                try:
                    req = urllib.request.Request(self.url)
                    url_open = urllib.request.urlopen(req)
                    data = url_open.read().decode('utf-8',errors='ignore')
                except Exception as e:
                    print(str(e) + '; check your Series ID')
                    sys.exit()

                ##Put Data into Pandas DataFrame
                data = json.loads(data)
                df = p.io.json.json_normalize(data['seriess'])
                df = df.convert_objects(convert_dates=True,
                                        convert_numeric=True)

                temp_time_type = df.frequency_short.values[0]

                if temp_time_type == 'A':
                    temp_time_type = 0
                elif temp_time_type == 'Q':
                    temp_time_type = 1
                elif temp_time_type == 'M':
                    temp_time_type = 2
                elif temp_time_type == 'W':
                    temp_time_type = 3
                elif temp_time_type == 'D':
                    temp_time_type = 4
                else:
                    temp_time_type = 'UNKNOWN'

                if temp_time_type < self.time_type:
                    self.time_type = temp_time_type

    ##Get Series Observations##
    def observations(self):

        root_url = ('https://api.stlouisfed.org/fred/series/'
                    + 'observations?series_id=')

        if type(self.series_id) == list:

            total_df = p.DataFrame()

            if self.time_type == 0:

                for x in self.series_id:

                    self.file_type = 'json'
                    self.url = (root_url+ x + '&api_key=' + self.FRED_API_Key
                                + '&file_type=' + self.file_type)
                               
                    ##Get the Data
                    try:
                        req = urllib.request.Request(self.url)
                        url_open = urllib.request.urlopen(req)
                        data = url_open.read().decode('utf-8',errors='ignore')
                    except Exception as e:
                        print(e)
                        sys.exit()

                    ##Put Data into Pandas DataFrame
                    data = json.loads(data)
                    df = p.io.json.json_normalize(data['observations'])
                    df = df.convert_objects(convert_dates=True,
                                            convert_numeric=True)
                    df['date'] = p.to_datetime(df['date'])
                    df.index = df.date
                    df = df.drop(['realtime_end', 'realtime_start', 'date'],
                                 axis=1)
                    df.columns = [x]
                    df = df.dropna()

                    ##Bring up data to the desired time periods
                    df = df.resample('A', how='mean')

                    if total_df.empty:
                        total_df = df
                    else:
                        total_df = total_df.merge(df,left_index=True,
                                                  right_index=True)

                return total_df

            elif self.time_type == 1:

                for x in self.series_id:

                    self.file_type = 'json'
                    self.url = (root_url + x + '&api_key=' + self.FRED_API_Key
                                + '&file_type=' + self.file_type)
                               
                    ##Get the Data
                    try:
                        req = urllib.request.Request(self.url)
                        url_open = urllib.request.urlopen(req)
                        data = url_open.read().decode('utf-8',errors='ignore')
                    except Exception as e:
                        print(e)
                        sys.exit()

                    ##Put Data into Pandas DataFrame
                    data = json.loads(data)
                    df = p.io.json.json_normalize(data['observations'])
                    df = df.convert_objects(convert_dates=True,
                                            convert_numeric=True)
                    df['date'] = p.to_datetime(df['date'])
                    df.index = df.date
                    df = df.drop(['realtime_end', 'realtime_start', 'date'],
                                 axis=1)
                    df.columns = [x]
                    df = df.dropna()

                    ##Bring up data to the desired time periods
                    df = df.resample('QS', how='mean')

                    if total_df.empty:
                        total_df = df
                    else:
                        total_df = total_df.merge(df,
                                                  left_index=True,
                                                  right_index=True)

                return total_df

            elif self.time_type == 2:

                for x in self.series_id:

                    self.file_type = 'json'
                    self.url = (root_url + x + '&api_key=' + self.FRED_API_Key
                                + '&file_type=' + self.file_type)
                               
                    ##Get the Data
                    try:
                        req = urllib.request.Request(self.url)
                        url_open = urllib.request.urlopen(req)
                        data = url_open.read().decode('utf-8',errors='ignore')
                    except Exception as e:
                        print(e)
                        sys.exit()

                    ##Put Data into Pandas DataFrame
                    data = json.loads(data)
                    df = p.io.json.json_normalize(data['observations'])
                    df = df.convert_objects(convert_dates=True,
                                            convert_numeric=True)
                    df['date'] = p.to_datetime(df['date'])
                    df.index = df.date
                    df = df.drop(['realtime_end', 'realtime_start', 'date'],
                                 axis=1)
                    df.columns = [x]
                    df = df.dropna()

                    ##Bring up data to the desired time periods
                    df = df.resample('M', how='mean')

                    if total_df.empty:
                        total_df = df
                    else:
                        total_df = total_df.merge(df,
                                                  left_index=True,
                                                  right_index=True)

                return total_df

            elif self.time_type == 3:

                for x in self.series_id:

                    self.file_type = 'json'
                    self.url = (root_url + x + '&api_key=' + self.FRED_API_Key
                                + '&file_type=' + self.file_type)
                               
                    ##Get the Data
                    try:
                        req = urllib.request.Request(self.url)
                        url_open = urllib.request.urlopen(req)
                        data = url_open.read().decode('utf-8',errors='ignore')
                    except Exception as e:
                        print(e)
                        sys.exit()

                    ##Put Data into Pandas DataFrame
                    data = json.loads(data)
                    df = p.io.json.json_normalize(data['observations'])
                    df = df.convert_objects(convert_dates=True,
                                            convert_numeric=True)
                    df['date'] = p.to_datetime(df['date'])
                    df.index = df.date
                    df = df.drop(['realtime_end', 'realtime_start', 'date'],
                                 axis=1)
                    df.columns = [x]
                    df = df.dropna()

                    ##Bring up data to the desired time periods
                    df = df.resample('W', how='mean')

                    if total_df.empty:
                        total_df = df
                    else:
                        total_df = total_df.merge(df,left_index=True,
                                                  right_index=True)

                return total_df

            elif self.time_type == 4:

                for x in self.series_id:

                    self.file_type = 'json'
                    self.url = (root_url + x + '&api_key=' + self.FRED_API_Key
                                + '&file_type=' + self.file_type)
                               
                    ##Get the Data
                    try:
                        req = urllib.request.Request(self.url)
                        url_open = urllib.request.urlopen(req)
                        data = url_open.read().decode('utf-8',errors='ignore')
                    except Exception as e:
                        print(e)
                        sys.exit()

                    ##Put Data into Pandas DataFrame
                    data = json.loads(data)
                    df = p.io.json.json_normalize(data['observations'])
                    df = df.convert_objects(convert_dates=True,
                                            convert_numeric=True)
                    df['date'] = p.to_datetime(df['date'])
                    df.index = df.date
                    df = df.drop(['realtime_end', 'realtime_start', 'date'],
                                 axis=1)
                    df.columns = [x]
                    df = df.dropna()

                    if total_df.empty:
                        total_df = df
                    else:
                        total_df = total_df.merge(df,left_index=True,
                                                  right_index=True)

                return total_df

            else:

                return 'Unknown Time Type'
       
        else:

            self.file_type = 'json'
            self.url = (root_url + x + '&api_key=' + self.FRED_API_Key
                        + '&file_type=' + self.file_type)
                       
            ##Get the Data
            try:
                req = urllib.request.Request(self.url)
                url_open = urllib.request.urlopen(req)
                data = url_open.read().decode('utf-8', errors='ignore')
            except Exception as e:
                print(e)
                sys.exit()

            ##Put Data into Pandas DataFrame
            data = json.loads(data)
            df = p.io.json.json_normalize(data['observations'])
            df = df.convert_objects(convert_dates=True, convert_numeric=True)
            df['date'] = p.to_datetime(df['date'])
            df.index = df.date
            df = df.drop(['realtime_end', 'realtime_start', 'date'], axis=1)
            df.columns = [self.series_id]
            df = df.dropna()

            return df

def shiller_cape():
    ##Get Shiller's CAPE Data
    location = 'http://www.econ.yale.edu/~shiller/data/ie_data.xls'
    
    try:
        df = p.read_excel(location,sheetname='Data',header=7)
    except Exception as e:
        print(e)
        sys.exit()
            
    df = df[np.isfinite(df.CAPE)]
    df = df.dropna(axis=1, how='all')
    index = p.date_range('1881-1-1', periods=df.CAPE.shape[0], freq='M')
    df = df.drop(['Date','Fraction'], axis=1)
    df_columns = ['NPrice','NDiv','NEarnings','CPI','GS10_Rate',
                  'RPrice', 'RDiv', 'REarnings', 'CAPE']
    df.columns = df_columns
    df.index = index
    
    return df

def yahoo_sp(stock_symbol):
    ##Stock price information from yahoo finance.
    try:
        req = urllib.request.Request('http://finance.yahoo.com/q/hp?s='
                                     + stock_symbol
                                     + '+Historical+Prices')
        yahoo_url = urllib.request.urlopen(req)
        yahoo_url_text = yahoo_url.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(e)
        sys.exit()

    if yahoo_url_text.find('Download to Spreadsheet') != -1:
        ##Parse the html text to get the csv url
        link_text = yahoo_url_text.find('Download to Spreadsheet')
        yahoo_url_text1 = yahoo_url_text[:link_text]
        url_start = yahoo_url_text1.rfind('<a href="') + len('<a href="')
        yahoo_url_text2 = yahoo_url_text1[url_start:]
        url_end = yahoo_url_text2.find('">')
        url_address = yahoo_url_text2[:url_end]

        ##Create a data frame from csv
        stock_df = p.DataFrame.from_csv(url_address, sep=',')

        ##Add a date column
        stock_df['close_date'] = stock_df.index

        ##Add a symbol column
        stock_df['symbol'] = stock_symbol

        return stock_df

    else:

        stock_df = p.DataFrame()
        return stock_df
