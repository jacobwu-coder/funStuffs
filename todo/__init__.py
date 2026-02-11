"""todo.py — simple CLI todo application

Usage examples:
  # add a new todo
  python todo.py add "Buy milk"

  # list pending todos
  python todo.py list --pending

  # mark todo #1 done
  python todo.py done 1

  # remove todo #2
  python todo.py remove 2

  # search todos containing "buy"
  python todo.py search buy

Notes:
- Stores data at ~/.local/share/funstuff/todos.json by default
- No external dependencies (only standard library)
"""
import argparse
import json
import os
import sys
from datetime import datetime

DEFAULT_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "funstuff")
DEFAULT_FILE = os.path.join(DEFAULT_DIR, "todos.json")


def ensure_storage(path=DEFAULT_FILE):
    d = os.path.dirname(path) or '.'
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump([], fh)


def load_todos(path=DEFAULT_FILE):
    ensure_storage(path)
    with open(path, "r", encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except Exception:
            return []


def save_todos(todos, path=DEFAULT_FILE):
    ensure_storage(path)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(todos, fh, indent=2, ensure_ascii=False)


def add_todo(text, path=DEFAULT_FILE):
    todos = load_todos(path)
    next_id = (max([t.get("id", 0) for t in todos]) + 1) if todos else 1
    item = {
        "id": next_id,
        "text": text,
        "created": datetime.utcnow().isoformat() + "Z",
        "done": False,
        "done_at": None,
    }
    todos.append(item)
    save_todos(todos, path)
    print(f"Added [{next_id}] {text}")


def list_todos(show_all=False, show_done=False, path=DEFAULT_FILE):
    todos = load_todos(path)
    if not todos:
        print("No todos found.")
        return
    if show_all:
        filtered = todos
    elif show_done:
        filtered = [t for t in todos if t.get("done")]
    else:
        filtered = [t for t in todos if not t.get("done")]

    for t in filtered:
        status = "x" if t.get("done") else " "
        print(f"[{t.get('id')}] [{status}] {t.get('text')}")


def mark_done(todo_id, path=DEFAULT_FILE):
    todos = load_todos(path)
    for t in todos:
        if t.get("id") == todo_id:
            if t.get("done"):
                print(f"Todo [{todo_id}] already done.")
                return
            t["done"] = True
            t["done_at"] = datetime.utcnow().isoformat() + "Z"
            save_todos(todos, path)
            print(f"Marked [{todo_id}] done.")
            return
    print(f"Todo [{todo_id}] not found.")


def remove_todo(todo_id, path=DEFAULT_FILE):
    todos = load_todos(path)
    new = [t for t in todos if t.get("id") != todo_id]
    if len(new) == len(todos):
        print(f"Todo [{todo_id}] not found.")
        return
    save_todos(new, path)
    print(f"Removed [{todo_id}].")


def clear_completed(path=DEFAULT_FILE):
    todos = load_todos(path)
    new = [t for t in todos if not t.get("done")]
    save_todos(new, path)
    print(f"Cleared completed todos. ({len(todos)-len(new)} removed)")


def search_todos(query, path=DEFAULT_FILE):
    todos = load_todos(path)
    found = [t for t in todos if query.lower() in t.get("text", "").lower()]
    if not found:
        print("No matches.")
        return
    for t in found:
        status = "x" if t.get("done") else " "
        print(f"[{t.get('id')}] [{status}] {t.get('text')}")


def build_parser():
    p = argparse.ArgumentParser(description="funStuff — simple CLI todo app")
    sub = p.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", nargs="+", help="Todo text")

    p_list = sub.add_parser("list", help="List todos")
    group = p_list.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="Show all todos")
    group.add_argument("--done", action="store_true", help="Show done todos")

    p_done = sub.add_parser("done", help="Mark todo as done")
    p_done.add_argument("id", type=int, help="Todo id")

    p_remove = sub.add_parser("remove", help="Remove a todo")
    p_remove.add_argument("id", type=int, help="Todo id")

    p_clear = sub.add_parser("clear-completed", help="Remove completed todos")

    p_search = sub.add_parser("search", help="Search todos")
    p_search.add_argument("query", help="Search query")

    p.add_argument("--file", default=DEFAULT_FILE, help="Path to todos.json")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    cmd = args.cmd
    path = args.file

    if cmd == "add":
        text = " ".join(args.text)
        add_todo(text, path)
    elif cmd == "list":
        list_todos(show_all=args.all, show_done=args.done, path=path)
    elif cmd == "done":
        mark_done(args.id, path)
    elif cmd == "remove":
        remove_todo(args.id, path)
    elif cmd == "clear-completed":
        clear_completed(path)
    elif cmd == "search":
        search_todos(args.query, path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
