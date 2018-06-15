#Script to Download and Merge the Freight Register(TMS Queries) and Traffic Earnings(RMS Queries)
#Written by Nawed Imroze (nawedx)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

import traffic_earning_download

import freight_register_download

import merger
