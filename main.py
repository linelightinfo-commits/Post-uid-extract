from flask import Flask, render_template_string, request
import re
import requests

app = Flask(__name__)

HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>FB Post UID Extractor</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', sans-serif;
      background-color: #0d0d0d;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      min-height: 100vh;
      color: white;
    }

    .glass-box {
      background: rgba(20, 20, 20, 0.9);
      border-radius: 20px;
      padding: 30px;
      width: 90%;
      max-width: 500px;
      box-shadow: 0 0 20px rgba(255, 0, 0, 0.7), 0 0 40px rgba(255, 0, 0, 0.4);
      border: 2px solid rgba(255, 0, 0, 0.8);
      text-align: center;
    }

    h2 {
      color: #ff5555;
      text-shadow: 0 0 10px red;
    }

    input[type=text] {
      width: 100%;
      padding: 12px;
      margin: 15px 0;
      border: none;
      border-radius: 8px;
      font-size: 16px;
      background-color: rgba(255,255,255,0.1);
      color: white;
      outline: none;
    }

    button {
      padding: 12px 25px;
      border: none;
      border-radius: 8px;
      background-color: #ff0033;
      color: white;
      font-size: 16px;
      cursor: pointer;
      box-shadow: 0 0 10px #ff0033;
      transition: background 0.3s, transform 0.2s;
    }

    button:hover {
      background-color: #cc0022;
      transform: scale(1.05);
    }

    .result {
      margin-top: 20px;
      font-weight: bold;
      color: #00ffcc;
      text-shadow: 0 0 5px black;
    }

    .footer {
      margin-top: 30px;
      font-size: 18px;
      font-weight: bold;
      color: #ff69b4;
      text-shadow: 0 0 10px black, 0 0 15px #ff69b4;
    }
  </style>
</head>
<body>
  <div class="glass-box">
    <h2>FB Post UID Extractor</h2>
    <form method="POST">
      <input type="text" name="fb_url" placeholder="Enter FB post URL" required>
      <button type="submit">Extract UID</button>
    </form>
    {% if uid %}
    <div class="result">Post UID: {{ uid }}</div>
    {% endif %}
    <div class="footer">2025 Code by Alex Khan</div>
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    uid = None
    if request.method == 'POST':
        fb_url = request.form['fb_url']
        try:
            resp = requests.get(fb_url)
            text = resp.text
            patterns = [
                r"/posts/(\d+)",
                r"story_fbid=(\d+)",
                r"""facebook\.com.*?/photos/\d+/(\d+)"""
            ]
            for pat in patterns:
                match = re.search(pat, text)
                if match:
                    uid = match.group(1)
                    break
        except Exception as e:
            uid = f"Error: {e}"
    return render_template_string(HTML, uid=uid)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
