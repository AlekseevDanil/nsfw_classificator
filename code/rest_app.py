from flask import Flask
import main

app = Flask(__name__)


@app.route('/')
def result():
    return 'hello, friend!'


@app.route('/check/<video>')
def check(video):
    input_vid = "../movies/" + video

    Neutral_percent, Porn_percent, Sexy_percent = main.start_classification(input_vid)

    return f'''Neutral = {Neutral_percent}% Porn = {Porn_percent} %Sexy = {Sexy_percent}%'''


if __name__ == '__main__':
    app.run(port=8000,
            host='127.0.0.1',
            debug=True)
