"""
Landing page
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3


st.markdown("# Home")


st.sidebar.markdown('''
Contains a brief overview of your Twitter ad activity from your archive.''')

con = sqlite3.connect("adimpressions.db")
cur = con.cursor()

dates= cur.execute('''select strftime('%Y', json_extract(impression,'$."impressionTime"')) || "-"|| 
        strftime('%m', json_extract(impression,'$."impressionTime"')) || "-" ||
        strftime('%d', json_extract(impression,'$."impressionTime"')) as Day
from rawjson  
group by Day
order by Day''').fetchall()

nradvertisers = cur.execute('''select count(distinct advertiser) as nrcorps from
(select  json_extract(impression, '$."advertiserInfo"."advertiserName"') as advertiser
from rawjson)
''').fetchone()[0]

nrads = cur.execute('''select count(impression)from rawjson''').fetchone()[0]


st.markdown(f'''This dataset has ad data from {dates[0][0]} to {dates[-1][0]}.''')

st.markdown('During that time, you were…')
st.markdown(f'''* …targeted by {nradvertisers:,} advertisers.
* …shown {nrads:,} ads.''')

st.markdown('For more details, explore the other pages!')
con.close()
