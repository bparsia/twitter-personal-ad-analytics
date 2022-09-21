"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import sqlite3



st.markdown('# Time')
st.sidebar.markdown('How ads vary with time')
#st.bar_chart(pd.read_csv('st_ad_app/pages/monthcount.csv'), x='Day', y='Ads Shown')
#st.table(pd.read_csv('st_ad_app/pages/monthcount.csv'))

con = sqlite3.connect("adimpressions.db")
byday = pd.read_sql_query('''select strftime('%Y', json_extract(impression,'$."impressionTime"')) as Year,    
        strftime('%m', json_extract(impression,'$."impressionTime"')) || "-" ||
		
        strftime('%d', json_extract(impression,'$."impressionTime"')) as Day, 
        count(impression) as "Ads Shown"
from rawjson  
group by Day
order by  Day''', con)

byhour = pd.read_sql_query('''select strftime('%H', json_extract(impression,'$."impressionTime"')) as Hour,
         count(impression) as "Ads Shown"
from rawjson  
group by Hour
order by Hour
''', con)
con.close()

st.bar_chart(byday,  x='Day', y='Ads Shown')

st.bar_chart(byhour,  x='Hour', y='Ads Shown')