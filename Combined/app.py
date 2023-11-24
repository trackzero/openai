from flask import Flask, render_template
import sys
import os
#sys.path.append("e:\\repos\\openai\\Combined")
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#print(sys.path)
from vision import vision_app
from dalle import dalle_app


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
#app.config['VISION_UPLOAD_FOLDER'] = 'vision_uploads'

@app.route('/')
def index():
    return render_template('index.html')

# Register blueprints
app.register_blueprint(vision_app, url_prefix='/vision')
app.register_blueprint(dalle_app, url_prefix='/dalle')

if __name__ == "__main__":

    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(rule)
    app.run(host='0.0.0.0', port=5050, debug=True)