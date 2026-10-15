# TaskBoard

TaskBoard is a small in-memory task API built with FastAPI.

## Run the app

Start the server from the project directory:

```sh
uv run taskboard
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API
documentation. Task data resets whenever the server restarts.

## API

- `GET /tasks` lists tasks; optionally filter with `?status=open` or `?status=done`
  and limit the number returned with `?limit=20`.
- `GET /tasks/{task_id}` retrieves one task.
- `POST /tasks` creates a task with a JSON body such as
  `{"title":"Review the RFC","priority":"high"}`. Status defaults to `open`;
  priority defaults to `medium`.
