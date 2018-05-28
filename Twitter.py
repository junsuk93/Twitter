from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/main', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        # first = request.form['First']
        # second = request.form['Second']
        result = request.form
        return render_template('main.html', result=result)


if __name__ == '__main__':
    app.run()
