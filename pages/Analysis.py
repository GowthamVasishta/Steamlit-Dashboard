# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 22:57:50 2024

@author: gowth
"""

import streamlit as st
import json
from helpers import common, loaders

# Call the function to inject the CSS
loaders.load_css("public/css/styles.css")

common.display_sidebar()

common.display_navbar()


# Backend data
data = {
    "labels": ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    "values": [12, 19, 3, 5, 2, 3]
}

# Render HTML
html_content = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <canvas id="myChart" width="400" height="200"></canvas>
    <script>
        let chartData = JSON.parse(`{{ data }}`);
        
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: '# of Votes',
                    data: chartData.values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
        });
    </script>
</body>
</html>
"""

# Replace placeholder with actual data
html_content = html_content.replace("{{ data }}", json.dumps(data))

# Embed HTML
st.components.v1.html(html_content, height=400)
