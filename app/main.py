from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.database import get_db, init_db
import os
import shutil
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles



class LoginInput(BaseModel):
    username: str
    password: str

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Welcome</h2>
    <a href='/register'>Register</a><br>
    <a href='/login'>Login</a><br>
    <a href='/upload'>Upload File</a><br>
    <a href='/view'>View Uploaded Files</a>
    """

@app.get("/register", response_class=HTMLResponse)
def register_form():
    return """
    <h3>Register</h3>
    <form action="/register" method="post">
        Username: <input name="username"><br>
        Password: <input name="password"><br>
        <button type="submit">Register</button>
    </form>
    """

@app.post("/register", response_class=HTMLResponse)
def register(username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        return f"<h4>Error: {e}</h4>"
    return "<h3>Registered!</h3><a href='/'>Home</a>"

@app.get("/login", response_class=HTMLResponse)
def login_form():
    return """
    <h3>Login</h3>
    <form action="/login" method="post">
        Username: <input name="username"><br>
        Password: <input name="password"><br>
        <button type="submit">Login</button>
    </form>
    """

@app.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    # query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    # result = cursor.execute(query).fetchone()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        return f"<h3>Welcome, {result[1]}!</h3>"
    return "<h3>Invalid credentials</h3><a href='/login'>Try again</a>"

@app.get("/upload", response_class=HTMLResponse)
def upload_form():
    return """
    <h3>Upload File (e.g., HTML with script)</h3>
    <form action="/upload" enctype="multipart/form-data" method="post">
        <input type="file" name="file"><br>
        <button type="submit">Upload</button>
    </form>
    """

@app.post("/upload", response_class=HTMLResponse)
def upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    ext = os.path.splitext(file.filename)[1].lower()
    FORBIDDEN_EXTENSIONS = {".html", ".htm", ".js", ".php", ".exe", ".sh", ".bat"}

    if ext in FORBIDDEN_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Files with extension '{ext}' are not allowed")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return f"<h3>File uploaded to /uploads/{file.filename}</h3><a href='/view'>View Files</a>"

@app.get("/view", response_class=HTMLResponse)
def view_files():
    files = os.listdir(UPLOAD_DIR)
    links = "<br>".join([f"<a href='/uploads/{f}' target='_blank'>{f}</a>" for f in files])
    return f"<h3>Uploaded Files:</h3>{links}"
