from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv('vars.env')

app = Flask(__name__)

api_key = os.getenv('VSCROSSING_API_KEY')


@app.route('/')
def index():
    print(api_key)
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    date1 = request.form['date1']
    date2 = request.form['date2']

    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date1}/{date2}?key={api_key}'
    response = requests.get(url)
    
    data = response.json()

    if response.status_code == 200:
        weather = [{
            'date': day['datetime'],
            'temp': day['temp'],
            'tempmax': day['tempmax'],
            'tempmin': day['tempmin'],
            'conditions': day['conditions'],
            'humidity': day['humidity'],
            'windspeed': day['windspeed'],
            'precip': day.get('precip', 0),
        }
            for day in data['days']
        ]

        return render_template('result.html', weather=weather, city=city)
    else:
        return render_template('error.html', error=data['message'])

if __name__ == '__main__':
    app.run(debug=True)