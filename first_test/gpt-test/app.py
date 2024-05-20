from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Index.html') 

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    qr_data = data.get('data')
    print(f"Received QR data: {qr_data}")
    # Process the QR code data as needed
    return jsonify({'status': 'success', 'data': qr_data})

@app.route('/hello_world')
def hello_world():
    return '''<h1> hello world </h1>'''

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')