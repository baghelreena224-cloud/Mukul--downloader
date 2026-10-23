from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Viral Video Downloader is Live!"

if __name__ == '__main__':
    app.run(debug=True)
