from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/report')
def report():
    return render_template('report.html')

if __name__ == '__main__':
    app.run()
