import sys
from main import main as app_main


def test_main_default(capsys, monkeypatch):
    # Run with no args -> should greet World
    monkeypatch.setattr(sys, 'argv', ['main.py'])
    app_main.main()
    captured = capsys.readouterr()
    assert 'Hello, World! funStaff is ready.' in captured.out


def test_main_name(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['main.py', '--name', 'Jacob'])
    app_main.main()
    captured = capsys.readouterr()
    assert 'Hello, Jacob! funStaff is ready.' in captured.out
