from flask import Flask, render_template
import sys
sys.path.append("e:\\repos\\openai\\Combined")
print(sys.path)

from .vision import vision_app
from .dalle import dalle_app
#sys.path.append("e:\repos\openai\Combined")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Register blueprints
app.register_blueprint(vision_app, url_prefix='/vision')
app.register_blueprint(dalle_app, url_prefix='/dalle')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)