from datetime import datetime
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import db

app = FastAPI(title="hspt_ai1 로그인 시스템", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"


class LoginRequest(BaseModel):
    userId: str
    userPasswd: str


def load_template(filename: str) -> str:
    file_path = TEMPLATES_DIR / filename
    with open(file_path, "r", encoding="utf-8-sig") as f:
        return f.read()


def render_login_page(error_message: Optional[str] = None, user_id: str = "") -> str:
    template = load_template("login.html")
    if error_message:
        alert_html = f"""<div class="alert"><span>{error_message}</span></div>"""
    else:
        alert_html = ""
    return template.replace("{{ERROR_ALERT}}", alert_html).replace("{{USER_ID}}", user_id)


def render_success_page(user: dict) -> str:
    template = load_template("success.html")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_name = str(user.get("userName") or "회원")
    user_id = str(user.get("userId") or "-")
    user_no = str(user.get("userNo") or "-")

    rendered = (
        template.replace("{{USER_NAME}}", user_name)
        .replace("{{USER_ID}}", user_id)
        .replace("{{USER_NO}}", user_no)
        .replace("{{LOGIN_TIME}}", now_str)
    )
    return rendered


@app.get("/", response_class=HTMLResponse)
async def login_page():
    return HTMLResponse(content=render_login_page(), status_code=200)


@app.post("/login", response_class=HTMLResponse)
async def handle_login(
    userId: str = Form(...),
    userPasswd: str = Form(...),
):
    user = db.authenticate_user(userId, userPasswd)
    if not user:
        return HTMLResponse(
            content=render_login_page(
                error_message="아이디 또는 비밀번호가 올바르지 않습니다.",
                user_id=userId,
            ),
            status_code=401,
        )
    return HTMLResponse(content=render_success_page(user), status_code=200)


@app.post("/api/login")
async def api_login(payload: LoginRequest):
    user = db.authenticate_user(payload.userId, payload.userPasswd)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
        )
    return {"success": True, "user": user}


@app.get("/api/health")
async def api_health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

