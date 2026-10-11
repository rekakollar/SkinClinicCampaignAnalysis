# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 12:16:26 2026

@author: T
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import numpy as np
import pandas as pd

app = FastAPI()

def run_campaign_analysis():
    
    df = pd.read_csv("skin clinic campaign.csv")
    
    gender_response = (
    df.groupby('Gender', observed =True)['Response_to_Campaign']
    .apply(lambda x: (x == 'Yes').mean() * 100)
    .round(2)
    .reset_index(name='Response Rate (%)')
    )
    
    age_group_response = (
    df.groupby('AgeGroup', observed =True)['Response_to_Campaign']
    .apply(lambda x: (x == 'Yes').mean() * 100)
    .round(2)
    .reset_index(name='Response Rate (%)')
    )
    
    last_quarter_response = (
    df.groupby('Purchase_Last_Quarter', observed =True)['Response_to_Campaign']
    .apply(lambda x: (x == 'Yes').mean() * 100)
    .round(2)
    .reset_index(name='Response Rate (%)')
    )
    
    df['Unique_Product_Category'] = pd.cut(
    df['Unique_Products_Purchased'],
    bins=[0, 4, 8, np.inf],
    labels=['1-4','5-8','>8']
    )
    
    unique_product_category_response_rate = (
    df.groupby('Unique_Product_Category', observed =True)['Response_to_Campaign']
    .apply(lambda x: (x == 'Yes').mean() * 100)
    .round(2)
    .reset_index(name='Response Rate (%)')
    )
    
    return {
        "Gender Response Rate": gender_response.to_dict(orient="records"),
        "Age Group Response Rate": age_group_response.to_dict(orient="records"),
        "Purchase in Last Quarter Response Rate": last_quarter_response.to_dict(orient="records"),
        "Unique Product Category Response Rate": unique_product_category_response_rate.to_dict(orient="records"),
    }

@app.get("/campaign-analysis")
def campaign_analysis():
    return run_campaign_analysis()

@app.get("/", response_class=HTMLResponse)
def home():

    html_content = """
    <html>
    <head>
        <title>Skin Clinic Campaign Analysis</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 30px;
            }

            table {
                border-collapse: collapse;
                margin-bottom: 30px;
                width: 50%;
            }

            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: center;
            }

            th {
                background-color: #f2f2f2;
            }

            h2 {
                margin-top: 30px;
            }

            button {
                padding: 10px 20px;
                font-size: 16px;
            }
        </style>
    </head>

    <body>

        <h1>Skin Clinic Campaign Analysis</h1>

        <button onclick="loadData()">Load Analysis</button>

        <div id="results"></div>

        <script>

        async function loadData() {

            const response = await fetch('/campaign-analysis');
            const data = await response.json();

            let html = '';

            for (const section in data) {

                html += `<h2>${section}</h2>`;

                const records = data[section];

                if (records.length > 0) {

                    html += '<table>';

                    html += '<tr>';

                    for (const key in records[0]) {
                        html += `<th>${key}</th>`;
                    }

                    html += '</tr>';

                    records.forEach(record => {

                        html += '<tr>';

                        for (const key in record) {
                            html += `<td>${record[key]}</td>`;
                        }

                        html += '</tr>';
                    });

                    html += '</table>';
                }
            }

            document.getElementById('results').innerHTML = html;
        }

        </script>

    </body>
    </html>
    """

    return html_content