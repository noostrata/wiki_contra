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
        body { font-family: Arial, sans-serif; margin: 2em; }
        form { margin-bottom: 1em; }
        .result { background: #f0f0f0; padding: 1em; border-radius: 5px; }
    </style>
</head>
<body>
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
