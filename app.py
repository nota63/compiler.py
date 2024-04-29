from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_and_execute():
    data = request.get_json()
    code = data['code']
    try:
        result = subprocess.run(['python', '-c', code], capture_output=True, text=True, timeout=10)
        return jsonify({'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Timeout expired. The code took too long to execute.'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
