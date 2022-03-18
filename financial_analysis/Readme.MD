This project shows a bunch of techniques and operations for financial analysis of timeseries.
Using the scripts from this project, different analysis and transformations can be operated on an equity timeseries.
For example: kurtosis, F-average return, exponential moving average, relative maxima and minima, Bollinger bands, etc.
Those indicators being themselves time-series can be then easily plotted. 

Before running the scripts:
1. Be sure to run "python -m pip install -r requirements.txt" from your terminal, for all the packages your interpreter needs.
2. Get online an API key for Quandl (if you want to run the modules who use it), then create a file named "local_settings.py" in the same folder where the script reside.
3. Create a "local_settings.py" file on your local machine and write the following line in the file: QUANDL_APL_KEY = 'xxxxxxx'

This project was developed using python 3.8.0.

Further documentation is provided inside the single modules.
