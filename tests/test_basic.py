import importlib

def test_import_watch_notify():
    """Simply import the module to ensure it has no syntax errors."""
    module = importlib.import_module('watch_notify')
    assert hasattr(module, 'main')
