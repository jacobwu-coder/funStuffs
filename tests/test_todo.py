import os
import json
import tempfile
from todo import add_todo, load_todos, save_todos, clear_completed, mark_done, remove_todo, search_todos


def test_add_and_list(tmp_path, capsys):
    db = tmp_path / "todos.json"
    add_todo("Test item 1", path=str(db))
    add_todo("Test item 2", path=str(db))
    todos = load_todos(path=str(db))
    assert len(todos) == 2


def test_mark_done_and_clear(tmp_path, capsys):
    db = tmp_path / "todos.json"
    add_todo("Item A", path=str(db))
    add_todo("Item B", path=str(db))
    todos = load_todos(path=str(db))
    first_id = todos[0]["id"]
    mark_done(first_id, path=str(db))
    todos = load_todos(path=str(db))
    assert any(t.get("done") for t in todos)
    clear_completed(path=str(db))
    todos = load_todos(path=str(db))
    assert all(not t.get("done") for t in todos)


def test_remove_and_search(tmp_path, capsys):
    db = tmp_path / "todos.json"
    add_todo("Buy milk", path=str(db))
    add_todo("Read book", path=str(db))
    todos = load_todos(path=str(db))
    first_id = todos[0]["id"]
    remove_todo(first_id, path=str(db))
    todos = load_todos(path=str(db))
    assert len(todos) == 1
    # test search (capture output)
    search_todos("Read", path=str(db))
    captured = capsys.readouterr()
    assert "Read book" in captured.out
