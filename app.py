from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism():
    file = request.files['file']
    # Call external plagiarism checking API
    # Here we use a mock function for demonstration
    result = mock_plagiarism_check(file)
    return jsonify({'result': result})

def mock_plagiarism_check(file):
    # Mock function to simulate plagiarism checking
    return "No plagiarism detected"

if __name__ == '__main__':
    app.run(debug=True)
