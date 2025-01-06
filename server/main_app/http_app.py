from uuid import uuid4

# from cachetools import Cache
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from orchestration import category as category_orchestration
from orchestration import site as site_orchestration
from orchestration import user as user_orchestration
from utils.log import logging
from utils.utils import naive_utcnow
from views.main import UserView

# from traceback import format_exc, print_exc


origins = [
    # allow localhost (useful for local development)
    "http://localhost",
    # for react, vue, etc. running on a different port
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:50051",
    # allow 0.0.0.0 (if your frontend is running on that address)
    "http://0.0.0.0:3000",
    "http://0.0.0.0:8000",
    "http://0.0.0.0:50051",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:50051",
    # allow all origins (use carefully for production!)
    "*",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # list of allowed origins
    allow_origins=origins,
    # allow cookies and credentials to be included in requests
    allow_credentials=True,
    # allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],
    # allow all headers (including Content-Type, Authorization, etc.)
    allow_headers=["*"],
)

# global cache
# cache = Cache(maxsize=100)

logging.info("Starting server!")
# call the site Random Walk


@app.get("/")
async def root():
    # return {"status": "online"}
    return None


@app.post("/is_user_name_available")
async def is_user_name_available(info: Request):
    req_info = await info.json()
    user_name = req_info["user_name"]
    return await user_orchestration.is_user_name_available(user_name)


@app.post("/register")
async def register(info: Request):
    req_info = await info.json()
    user_view = UserView(
        uuid=uuid4(),
        user_name=req_info["user_name"],
        email=req_info["email"],
        password=req_info["password"],
        photo=None,
        role="default",
        joined_at=naive_utcnow(),
        last_login=naive_utcnow(),
    )
    return await user_orchestration.upsert_user(user_view)


@app.post("/login")
async def login(info: Request):
    req_info = await info.json()
    email = req_info["email"]
    password = req_info["password"]
    return await user_orchestration.login(email, password)


@app.get("/category-group/list")
async def category_group_list():
    return category_orchestration.list_all_category_groups()


@app.post("/category-group/like")
async def category_group_like(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    category_group_uuid = req_info["category_group_uuid"]
    return await category_orchestration.like_category_group(user_uuid, category_group_uuid)


@app.post("/category-group/dislike")
async def category_group_dislike(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    category_group_uuid = req_info["category_group_uuid"]
    return await category_orchestration.like_category_group(user_uuid, category_group_uuid)


@app.get("/category/list")
async def category_list(info: Request):
    req_info = await info.json()
    category_group_uuid = req_info["category_group_uuid"]
    return await category_orchestration.list_all_categories(category_group_uuid)


@app.post("/category/like")
async def category_like(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    category_uuid = req_info["category_uuid"]
    return await category_orchestration.like_category(user_uuid, category_uuid)


@app.post("/category/dislike")
async def category_dislike(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    category_uuid = req_info["category_uuid"]
    return category_orchestration.dislike_category(user_uuid, category_uuid)


@app.post("/site/visit")
async def site_visit(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    site_uuid = req_info["site_uuid"]
    return site_orchestration.visit_site(user_uuid, site_uuid)


@app.post("/site/like")
async def site_like(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    site_uuid = req_info["site_uuid"]
    return site_orchestration.like_site(user_uuid, site_uuid)


@app.post("/site/dislike")
async def site_dislike(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    site_uuid = req_info["site_uuid"]
    return site_orchestration.dislike_site(user_uuid, site_uuid)


@app.post("/sites/liked")
async def sites_liked(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    return site_orchestration.get_user_liked_sites(user_uuid)


@app.post("/sites/visited")
async def site_visited(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    return site_orchestration.get_user_visited_sites(user_uuid)


@app.post("/random_walk")
async def random_walk(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    return {"user_uuid": user_uuid}


@app.post("/site/flag")
async def site_flag(info: Request):
    req_info = await info.json()
    user_uuid = req_info["user_uuid"]
    site_uuid = req_info["site_uuid"]
    return {"user_uuid": user_uuid, "site_uuid": site_uuid}
