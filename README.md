# fastapi-imagekit

Simple Instagram-like backend (FastAPI) with ImageKit image uploads.

Quick start
1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` in the project root with these values:

```
IMAGEKIT_PRIVATE_KEY=private_xxx
IMAGEKIT_PUBLIC_KEY=public_xxx
IMAGEKIT_URL=https://ik.imagekit.io/your_path
# optional: DATABASE_URL=sqlite:///./database.db
```

3. Run the app (development):

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# or run the bundled starter
python main.py
```

Endpoints
- `POST /posts` — create a post (multipart form). Fields: `caption` (string), `image` (file).
- `GET /posts` — list recent posts.
- `GET /posts/{id}` — read a single post.
- `PUT /posts/{id}` — update a post (JSON body: `{ "caption": "..." }`).
- `DELETE /posts/{id}` — delete a post and its image in ImageKit.

Examples
- Create a post (multipart/form-data):

```bash
curl -X POST "http://localhost:8000/posts" \
	-F "caption=Hello world" \
	-F "image=@/path/to/photo.jpg"
```

- List posts:

```bash
curl http://localhost:8000/posts
```

- Get a post:

```bash
curl http://localhost:8000/posts/1
```

- Update a post's caption:

```bash
curl -X PUT "http://localhost:8000/posts/1" -H "Content-Type: application/json" \
	-d '{"caption":"updated caption"}'
```

- Delete a post:

```bash
curl -X DELETE http://localhost:8000/posts/1
```

Notes
- Make sure ImageKit keys in `.env` are valid; uploads and deletes use ImageKit API.
- The app uses SQLite by default (`database.db`) unless `DATABASE_URL` is set.

