from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        subprocess.run(['python', 'python/main.py'], check=True)
        result = 'Script executed successfully.'
    except subprocess.CalledProcessError:
        result = 'An error occurred while running the script.'
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run()