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

nrcategories = cur.execute('''select json_extract(criteria.value, '$."targetingType"') as criterion,
        count (criteria.value) as typeCount
from rawjson, json_each(impression, '$."matchedTargetingCriteria"') as criteria
group by criterion
order by  typeCount desc
limit 10''').fetchall()
cats = list()
nrs = list()

for c, n in nrcategories:
    cats.append(c)
    nrs.append(n)
    
nrcategories = pd.DataFrame({'Category':cats, 'Count':nrs})

st.markdown(f'''This dataset has ad data from {dates[0][0]} to {dates[-1][0]}.''')
st.markdown('During that time, you were…')
st.markdown(f'''* …targeted by {nradvertisers:,} advertisers.
* …shown {nrads:,} ads.''')
st.markdown('These are the top ten categories (by influence) of targeting criteria.')
st.write(nrcategories)
st.markdown('For more details, explore the other pages!')
con.close()
