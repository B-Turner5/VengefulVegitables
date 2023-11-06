from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/process_prompt', methods=['POST'])
def process_input():
    data = request.get_json()
    print(data)
    prompt = data.get('prompt')
    
    return "Input recieved by Flask"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)