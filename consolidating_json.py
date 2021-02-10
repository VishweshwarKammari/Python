import pandas as pd
import os
import glob
import sqlite3
import json

#setting up input and output paths:
ippath="s3://trivago-case-study/case-study-data/import/"
oppath="s3://trivago-case-study/case-study-data/output"

#setting up sqllite database for transformation sql logic
conn = sqlite3.connect("partner_data.db")
cur = conn.cursor()
#ippath= input path where the input files are located.
#oppath= output path where the consolidated files are located.
def consolidator(ippath, oppath):
#looping through all the files in the input path
    for filename in glob.glob(os.path.join(ippath, '*.json')):
        with open(os.path.join(os.getcwd(), filename), 'r') as nested_data:
            partner_data = json.load(nested_data)
#creating pandas dataframe from the source data.
    partner_datadf = pd.DataFrame(partner_data, columns=['partner_name', 'accommodation_id', 'accommodation_data'])
#normalizing data dataframe into a flat table.
    partner_datadf1 = pd.json_normalize(json.loads(partner_datadf.to_json(orient="records")))
#picking the required fields
    fields = ['partner_name', 'accommodation_id', 'accommodation_data.accommodation_name']
    partner_data_UnnestedDF = partner_datadf1[fields]
#giving proper names to columns
    partner_data_UnnestedDF.columns = ['partner_name', 'accommodation_id', 'accommodation_name']
#creating table from the dataframe
    cur.execute("DROP TABLE IF EXISTS partner_data_unnested")
    partner_data_UnnestedDF.to_sql('partner_data_unnested', conn)
#consolidation logic using SQllite query
    query = "SELECT partner_name,accommodation_id,accommodation_name FROM (SELECT partner_name,accommodation_id," \
            "accommodation_name,row_number() over(PARTITION BY accommodation_id ORDER BY partner_name) as " \
            "preferred_id FROM partner_data_unnested)a WHERE preferred_id=1 "
#writing the consolidated data to a dataframe.
    partner_data_preferred = pd.read_sql_query(query, conn)
#writing consolidated data into output path.
    partner_data_preferred.to_json(oppath, orient='records')
