import pandas as pd
import json
import plotly.graph_objects as pg
import plotly.express as px

# Load the JSON data
with open('eve.json') as file:
    data = [json.loads(line) for line in file]

# Convert to DataFrame
df = pd.json_normalize(data)

# Parse timestamps
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract relevant columns
df = df[['timestamp', 'alert.signature', 'alert.category', 'src_ip', 'dest_ip', 'dest_port']]

# Alerts over time
alerts_over_time = df.groupby(df['timestamp'].dt.floor('min')).size().reset_index(name='counts')

# Alerts by category
alerts_by_category = df['alert.category'].value_counts().reset_index()
alerts_by_category.columns = ['category', 'counts']

# Source IPs with most alerts
alerts_by_src_ip = df['src_ip'].value_counts().reset_index()
alerts_by_src_ip.columns = ['src_ip', 'counts']

# Destination ports targeted
alerts_by_dest_port = df['dest_port'].value_counts().reset_index()
alerts_by_dest_port.columns = ['dest_port', 'counts']

# Create the graphs

# Alerts Over Time
fig1 = pg.Figure()
fig1.add_trace(pg.Scatter(x=alerts_over_time['timestamp'], y=alerts_over_time['counts'], mode='lines', name='Alerts'))
fig1.update_layout(title='Alerts Over Time', xaxis_title='Time', yaxis_title='Number of Alerts', template='plotly_dark')

# Alerts by Category
fig2 = px.bar(alerts_by_category, x='category', y='counts', title='Alerts by Category', template='plotly_dark')

# Source IPs with Most Alerts
fig3 = px.bar(alerts_by_src_ip.head(10), x='src_ip', y='counts', title='Top 10 Source IPs by Alert Count', template='plotly_dark')

# Destination Ports Targeted
fig4 = px.pie(alerts_by_dest_port, values='counts', names='dest_port', title='Targeted Destination Ports', template='plotly_dark')

# Display the figures
fig1.show()
fig2.show()
fig3.show()
fig4.show()
