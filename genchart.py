
# pip3 install pandas
# pip3 install plotly

import json
import requests
import plotly.graph_objects as go
import plotly.express as px

from db import list_users, load_user_records

def upload_to_slack(file_path):
    with open('webhook.json', 'r') as f:
        cred = json.load(f)
    slack_token = cred['slack_token']
    file_to_upload = {
        'file' : (file_path, open(file_path, 'rb'), 'png')
    }

    payload={
        'filename': file_path, 
        'token': slack_token, 
        'channels': ['#exercise'], 
    }

    response = requests.post("https://slack.com/api/files.upload", params=payload, files=file_to_upload)
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.content)
    else:
        print('Uploade succeeded.')
    

fig = go.Figure()
users = list_users()
for user in users:
    timestamps, avg_times = [], []
    records = load_user_records(user)
    for r in records:
        total = r['correct'] + r['wrong']
        avg_time = float(r['duration']) / float(total)
        timestamps.append(r['timestamp'])
        avg_times.append(avg_time)

    fig.add_trace(go.Scatter(x=timestamps, y=avg_times,
                    mode='lines',
                    name=user))

fig.update_layout(title='Average Time Spent on Each Problem',
                   yaxis_title='Time (Seconds)')

fig.show()
fig.write_html('average_time.html', auto_open=False)
fig.write_image('average_time.png')
upload_to_slack('average_time.png')




