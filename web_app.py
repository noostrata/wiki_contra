from flask import Flask, render_template_string, request
from contropedia import fetch_revisions, analyze_reverts

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Contropedia Lite</title>
    <style>
        body {
            font-family: system-ui, sans-serif;
            background: #f6f8fa;
            display: flex;
            justify-content: center;
            padding: 2em;
        }
        .container {
            background: #fff;
            padding: 2em 3em;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            width: 28em;
        }
        form {
            display: flex;
            gap: 0.5em;
            margin-bottom: 1em;
        }
        input[type=text] {
            flex: 1;
            padding: 0.5em;
            font-size: 1em;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 0.5em 1em;
            border: none;
            background: #007bff;
            color: white;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
        .result {
            margin-top: 1em;
            background: #f0f8ff;
            padding: 1em;
            border-radius: 5px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Contropedia Lite</h1>
    <form method="get">
        <input type="text" name="title" placeholder="Article title" value="{{ title }}">
        <button type="submit">Analyze</button>
    </form>
    {% if result %}
    <div class="result">
        <p><strong>Article:</strong> {{ title }}</p>
        <p><strong>Total revisions fetched:</strong> {{ result.total }}</p>
        <p><strong>Detected reverts:</strong> {{ result.reverts }}</p>
        <p><strong>Controversy score:</strong> {{ result.score }}</p>
    </div>
    {% endif %}
</div>
</body>
</html>
"""

class Result:
    def __init__(self, total, reverts, score):
        self.total = total
        self.reverts = reverts
        self.score = score

@app.route('/', methods=['GET'])
def index():
    title = request.args.get('title', '')
    result = None
    if title:
        revisions = fetch_revisions(title)
        total = len(revisions)
        reverts = analyze_reverts(revisions)
        score = round(reverts / total, 3) if total else 0
        result = Result(total, reverts, score)
    return render_template_string(HTML_TEMPLATE, title=title, result=result)

if __name__ == '__main__':
    app.run(debug=True)
