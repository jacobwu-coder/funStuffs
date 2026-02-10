import sys
from funstuff import main as app_main


def test_main_default(capsys, monkeypatch):
    # Run with no args -> should greet World
    monkeypatch.setattr(sys, 'argv', ['main.py'])
    app_main.main()
    captured = capsys.readouterr()
    assert 'Hello, World! funstuff is ready.' in captured.out


def test_main_name(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['main.py', '--name', 'Jacob'])
    app_main.main()
    captured = capsys.readouterr()
    assert 'Hello, Jacob! funstuff is ready.' in captured.out
