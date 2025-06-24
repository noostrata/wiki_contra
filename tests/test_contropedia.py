import io
import json
import os
import sys
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import contropedia

class DummyResponse(io.StringIO):
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass

def test_fetch_revisions():
    data = {
        "query": {
            "pages": {
                "123": {
                    "revisions": [
                        {"timestamp": "2020", "user": "A", "comment": "first"}
                    ]
                }
            }
        }
    }
    response = DummyResponse(json.dumps(data))
    with mock.patch("contropedia.request.urlopen", return_value=response):
        revs = contropedia.fetch_revisions("Example", limit=1)
    assert revs == data["query"]["pages"]["123"]["revisions"]

def test_analyze_reverts():
    revisions = [
        {"comment": "reverted vandalism"},
        {"comment": "minor fix"},
        {"comment": "Undo previous revision"},
    ]
    assert contropedia.analyze_reverts(revisions) == 2
