from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
      <head><title>Dockerized Flask App</title></head>
      <body style="font-family: sans-serif; padding: 40px;">
        <h1>It's running in a container 🐳</h1>
        <p>This Flask app is serving requests from inside Docker.</p>
        <p>Try the JSON endpoint: <a href="/api/status">/api/status</a></p>
      </body>
    </html>
    """


@app.route("/api/status")
def status():
    return jsonify({"status": "ok", "service": "flask-docker-demo"})


if __name__ == "__main__":
    # host=0.0.0.0 is required so the app is reachable from outside the container
    app.run(host="0.0.0.0", port=5000, debug=False)
