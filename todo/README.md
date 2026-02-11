todo.py — CLI Todo App

Location: ./todo.py

Usage examples:
  # add a new todo
  python todo.py add "Buy milk"

  # list pending todos
  python todo.py list --pending

  # list all todos
  python todo.py list --all

  # mark todo #1 done
  python todo.py done 1

  # remove todo #2
  python todo.py remove 2

  # clear completed todos
  python todo.py clear-completed

  # search todos containing "buy"
  python todo.py search buy

Notes
- Data is stored at ~/.local/share/funstuff/todos.json by default.
- No external dependencies; standard library only.
- The repo also includes helper scripts: commit_and_push.sh, sync_from_upstream.sh
