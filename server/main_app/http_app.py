from uuid import uuid4

# from cachetools import Cache
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from orchestration import category as category_orchestration
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


# @app.get("/category/site/tag")
# async def category_group_like_all():
#     return {"status": "online"}


@app.get("/site/like")
async def site_like():
    return {"status": "online"}


@app.get("/random_walk")
async def random_walk():
    return {"status": "online"}


# @app.get("/is_trading_day")
# async def is_trading_day(exchange="XNYS", timestamp=None):
#     """
#     Finds out if the current datetime is a trading day for an given exchange.

#     Parameters
#     ----------
#     exchange : str
#         abbreviation for exchange, according to trading_calendars library
#     timestamp : datetime
#         datetime to check, if not specified then check current datetime

#     Returns
#     ----------
#     session : bool
#         True/False whether the current datetime is a trading day for an given exchange
#     """

#     now = get_datetime(city="UTC", mode="datetime")
#     if cache.get("is_trading_day-last_updated_hour") == now.hour:
#         status = cache["is_trading_day"]
#     else:
#         status = trading_calendar.is_trading_day(exchange=exchange, timestamp=timestamp)
#         cache["is_trading_day"] = status
#         cache["is_trading_day-last_updated_hour"] = now.hour
#     return {"is_trading_day": status}


# @app.get("/is_trading_session")
# async def is_trading_session(exchange="XNYS", extended_hours=False, timestamp=None):
#     """
#     Finds out if the current datetime is a trading session for an given exchange.

#     Parameters
#     ----------
#     exchange : str
#         abbreviation for exchange, according to trading_calendars library
#     extended_hours : bool
#         whether or not to trade during extended market hours
#     timestamp : datetime
#         datetime to check, if not specified then check current datetime

#     Returns
#     ----------
#     session : bool
#         True/False whether the current datetime is a trading session for an given exchange
#     """

#     now = get_datetime(city="UTC", mode="datetime")
#     if cache.get("is_trading_session-last_updated_hour_minute") == f"{now.hour}-{now.minute}":
#         status = cache["is_trading_session"]
#     else:
#         status = trading_calendar.is_trading_session(
#             exchange=exchange, extended_hours=extended_hours, timestamp=timestamp
#         )
#         cache["is_trading_session"] = status
#         cache["is_trading_session-last_updated_hour_minute"] = f"{now.hour}-{now.minute}"
#     return {"is_trading_session": status}


# @app.get("/exchange/parameters/load")
# async def exchange_read_parameters(parameters_path=PARAMETERS_PATH):
#     """
#     Load parameters from csv into cache.

#     Parameters
#     ----------
#     parameters_path : Path
#         path to parameters csv

#     Returns
#     ----------
#     None
#     """

#     with FileLock(parameters_path.with_suffix(parameters_path.suffix + ".lock")):
#         parameters_df = read_csv(parameters_path)
#     parameters_df = fillna(df=parameters_df)
#     cache["parameters_df"] = parameters_df


# @app.post("/exchange/parameters/get")
# async def exchange_get_parameters(info: Request):
#     """
#     Get parameters for given exchange, strategy, and pair.

#     Parameters
#     ----------
#     info : Request
#         JSON of info, like dict, must have have keys Exchange, Strategy, and Pair

#     Returns
#     ----------
#     parameters : dict
#         dict of parameter info
#     """

#     try:
#         req_info = await info.json()
#         parameters_df = cache["parameters_df"]
#         parameter_row = parameters_df.loc[
#             (parameters_df["Exchange"] == req_info["Exchange"])
#             & (parameters_df["Strategy"] == req_info["Strategy"])
#             & (parameters_df["Pair"] == req_info["Pair"])
#         ]
#         parameters = Series(parameter_row.loc[parameter_row.index[0], :])
#         parameters.fillna("", inplace=True)
#         return parameters.to_json()

#     except Exception:
#         print_exc()
#         er = format_exc()
#         return json.dumps({"error": er})


# @app.post("/exchange/parameters/get/all")
# async def exchange_get_parameters_df():
#     """
#     Get the entire parameters dataframe.

#     Parameters
#     ----------
#     None

#     Returns
#     ----------
#     parameters : dict
#         dict of parameter info
#     """

#     parameters_df = cache["parameters_df"]
#     parameters_df = fillna(df=parameters_df)
#     return parameters_df.to_json()


# @app.post("/exchange/parameters/reset_flag")
# async def exchange_parameter_reset_flag(info: Request, parameters_path=PARAMETERS_PATH):
#     """
#     Reset flag to Run for given exchange, strategy, and pair in parameters. Resets in cache and csv.

#     Parameters
#     ----------
#     info : Request
#         JSON of info, like dict, must have have keys Exchange, Strategy, and Pair
#     parameters_path : Path
#         path to parameters csv

#     Returns
#     ----------
#     None
#     """

#     try:
#         req_info = await info.json()
#         parameters_df = cache["parameters_df"]
#         parameters_df.loc[
#             (parameters_df["Exchange"] == req_info["Exchange"])
#             & (parameters_df["Strategy"] == req_info["Strategy"])
#             & (parameters_df["Pair"] == req_info["Pair"]),
#             "Flags",
#         ] = ""
#         cache["parameters_df"] = parameters_df
#         with FileLock(parameters_path.with_suffix(parameters_path.suffix + ".lock")):
#             parameters_df.to_csv(parameters_path, index=False)
#     except Exception:
#         print_exc()


# @app.get("/live_tracking/reports/running/load")
# async def live_tracking_read_running(running_path=RUNNING_PATH):
#     """
#     Load parameters from csv into cache.

#     Parameters
#     ----------
#     running_path : Path
#         path to running csv

#     Returns
#     ----------
#     None
#     """

#     with FileLock(running_path.with_suffix(running_path.suffix + ".lock")):
#         running_df = read_csv(running_path)
#     running_df = fillna(df=running_df)
#     cache["running_df"] = running_df


# @app.post("/live_tracking/reports/running/get")
# async def live_tracking_get_running(info: Request):
#     """
#     Get parameters for given exchange, strategy, and pair.

#     Parameters
#     ----------
#     info : Request
#         JSON of info, like dict, must have have keys Exchange, Strategy, and Pair

#     Returns
#     ----------
#     running : dict
#         dict of running info
#     """

#     try:
#         req_info = await info.json()
#         running_df = cache["running_df"]
#         running_row = running_df.loc[
#             (running_df["Exchange"] == req_info["Exchange"])
#             & (running_df["Strategy"] == req_info["Strategy"])
#             & (running_df["Pair"] == req_info["Pair"])
#         ]
#         running = Series(running_row.loc[running_row.index[0], :])
#         running.fillna("", inplace=True)
#         return running.to_json()

#     except Exception:
#         print_exc()
#         er = format_exc()
#         return json.dumps({"error": er})


# @app.post("/live_tracking/reports/running/get/all")
# async def live_tracking_get_running_df():
#     """
#     Get parameters for given exchange, strategy, and pair.

#     Parameters
#     ----------
#     None

#     Returns
#     ----------
#     running_df : dict
#         dict of running info
#     """

#     running_df = cache["running_df"]
#     running_df.reset_index(drop=True, inplace=True)
#     running_df = fillna(df=running_df)
#     return running_df.to_json()


# @app.post("/exchange/strategy/running/update")
# async def exchange_strategy_running(info: Request, running_path=RUNNING_PATH, id_cols=ID_COLS):
#     """
#     Add running strategy script to running csv.

#     Parameters
#     ----------
#     info : Request
#         JSON of info, like dict
#     running_path : Path
#         path to running csv
#     id_cols : list
#         list of column names that act as strategy unique identifier, Exchange, Strategy, and Pair

#     Returns
#     ----------
#     None
#     """

#     req_info = await info.json()
#     running_row = DataFrame([req_info.values()], columns=req_info.keys())
#     try:
#         now = get_datetime(city="UTC", mode="datetime")
#         if cache.get("running-last_updated_hour_minute") == f"{now.hour}-{now.minute}":
#             running_df = cache["running_df"]
#         else:
#             cache["running-last_updated_hour_minute"] = f"{now.hour}-{now.minute}"
#             with FileLock(running_path.with_suffix(running_path.suffix + ".lock")):
#                 running_df = read_csv(running_path)

#         running_df = concat([running_df, running_row])
#         running_df.sort_values(by=id_cols + ["Last Update"], ascending=[True, True, True, False], inplace=True)
#         running_df.drop_duplicates(subset=id_cols, keep="first", inplace=True)
#         running_df.reset_index(drop=True, inplace=True)
#         running_df = fillna(df=running_df)

#         cache["running_df"] = running_df
#         if cache.get("running-last_updated_hour_minute") == f"{now.hour}-{now.minute}":
#             with FileLock(running_path.with_suffix(running_path.suffix + ".lock")):
#                 running_df.to_csv(running_path, index=False)

#     except EmptyDataError:
#         running_row.to_csv(running_path, index=False)


# @app.post("/exchange/strategy/running/stop")
# async def exchange_strategy_stopped(info: Request, running_path=RUNNING_PATH, id_cols=ID_COLS):
#     """
#     Remove running strategy script from running csv.

#     Parameters
#     ----------
#     info : Request
#         JSON of request info, like dict
#     running_path : Path
#         path to running csv
#     id_cols : list
#         list of column names that act as strategy unique identifier, Exchange, Strategy, and Pair

#     Returns
#     ----------
#     None
#     """

#     req_info = await info.json()
#     try:
#         now = get_datetime(city="UTC", mode="datetime")
#         if cache.get("running-last_updated_hour_minute") == f"{now.hour}-{now.minute}":
#             running_df = cache["running_df"]
#         else:
#             cache["running-last_updated_hour_minute"] = f"{now.hour}-{now.minute}"
#             with FileLock(running_path.with_suffix(running_path.suffix + ".lock")):
#                 running_df = read_csv(running_path)

#         running_row = running_df.loc[
#             (running_df["Exchange"] == req_info["Exchange"])
#             & (running_df["Strategy"] == req_info["Strategy"])
#             & (running_df["Pair"] == req_info["Pair"])
#         ]
#         running_df.drop(index=running_row.index, inplace=True)
#         running_df.sort_values(by=id_cols + ["Last Update"], ascending=[True, True, True, False], inplace=True)
#         running_df.drop_duplicates(subset=id_cols, keep="first", inplace=True)
#         running_df.reset_index(drop=True, inplace=True)
#         running_df = fillna(df=running_df)

#         cache["running_df"] = running_df
#         if cache.get("running-last_updated_hour_minute") == f"{now.hour}-{now.minute}":
#             with FileLock(running_path.with_suffix(running_path.suffix + ".lock")):
#                 running_df.to_csv(running_path, index=False)

#     except EmptyDataError:
#         pass


# @app.get("/exchange/strategy/running/clear_cache")
# async def exchange_strategy_running_clear_cache():
#     """
#     Clear the running dateframe cache.

#     Parameters
#     ----------
#     None

#     Returns
#     ----------
#     None
#     """

#     del cache["running_df"]


# @app.post("/exchange/strategy/message/log")
# async def exchange_strategy_message_log(info: Request, msg: str, log_path: str):
#     """
#     Log message to log csv.

#     Parameters
#     ----------
#     info : Request
#         JSON of request info, like dict
#     msg : str
#         str message to log
#     log_path : Path
#         path to log file

#     Returns
#     ----------
#     None
#     """

#     req_info = await info.json()
#     log_path = Path(log_path)
#     exchange = req_info["Exchange"].lower().replace(" ", "_")
#     strategy = req_info["Strategy"].lower().replace(" ", "_")
#     if sum(x.isdigit() for x in strategy[-5:]) >= 3:
#         strategy = strategy[:-6]
#     log_cache_name = f"logs_df_{exchange}_{strategy}"
#     try:
#         try:
#             now = get_datetime(city="UTC", mode="datetime")
#             if (
#                 cache.get("message-last_updated_hour_minute") == f"{now.hour}-{now.minute}"
#                 and cache.get(log_cache_name) is not None
#             ):
#                 logs_df = cache[log_cache_name]
#             else:
#                 cache["message-last_updated_hour_minute"] = f"{now.hour}-{now.minute}"
#                 with FileLock(log_path.with_suffix(log_path.suffix + ".lock")):
#                     logs_df = read_csv(log_path)

#         except FileNotFoundError:
#             logs_df = DataFrame(columns=["Exchange", "Strategy", "Pair", "Last Update", "Message"])
#             logs_df.to_csv(log_path, index=False)
#             cache[log_cache_name] = logs_df

#         log_data = [
#             [
#                 req_info["Exchange"],
#                 req_info["Strategy"],
#                 req_info["Pair"],
#                 req_info["Last Update"],
#                 msg,
#             ]
#         ]
#         logs_df = concat([logs_df, DataFrame(log_data, columns=logs_df.columns)])
#         logs_df.sort_values(by=["Last Update"], ascending=[True], inplace=True)

#         cache[log_cache_name] = logs_df
#         if cache.get("message-last_updated_hour_minute") == f"{now.hour}-{now.minute}":
#             with FileLock(log_path.with_suffix(log_path.suffix + ".lock")):
#                 logs_df.to_csv(log_path, index=False)

#     except Exception:
#         print_exc()


# @app.get("/exchange/strategy/message/log/clear_cache")
# async def exchange_strategy_message_log_clear_cache():
#     """
#     Reset logs dataframe cache.

#     Parameters
#     ----------
#     None

#     Returns
#     ----------
#     None
#     """

#     for key in cache.keys():
#         if "logs_df" in key:
#             logs_df = DataFrame(columns=["Exchange", "Strategy", "Pair", "Last Update", "Message"])
#             cache[key] = logs_df


# @app.post("/exchange/strategy/returns/log")
# async def exchange_strategy_log_return(info: Request, returns_path=RETURNS_PATH):
#     """
#     Log return to returns csv.

#     Parameters
#     ----------
#     info : Request
#         JSON of request info, like dict
#     returns_path : Path
#         path to returns csv

#     Returns
#     ----------
#     None
#     """

#     req_info = await info.json()
#     try:
#         with FileLock(returns_path.with_suffix(returns_path.suffix + ".lock")):
#             returns_df = read_csv(returns_path)
#             returns_df.loc[
#                 (returns_df["Exchange"] == req_info["Exchange"])
#                 & (returns_df["Strategy"] == req_info["Strategy"])
#                 & (returns_df["Pair"] == req_info["Pair"]),
#                 "Return",
#             ] += req_info["Last Rtn"]
#             returns_df.to_csv(returns_path, index=False)
#     except Exception:
#         print_exc()


# @app.post("/exchange/strategy/returns_by_trade/log")
# async def exchange_strategy_log_return_by_trade(info: Request, returns_by_trade_path=RETURNS_BY_TRADE_PATH):
#     """
#     Log return to returns by trade csv.

#     Parameters
#     ----------
#     info : Request
#         JSON of request info, like dict
#     returns_path : Path
#         path to returns csv

#     Returns
#     ----------
#     None
#     """

#     req_info = await info.json()
#     try:
#         with FileLock(returns_by_trade_path.with_suffix(returns_by_trade_path.suffix + ".lock")):
#             returns_by_trade_df = read_csv(returns_by_trade_path)
#             trade_data = [
#                 [
#                     req_info["Exchange"],
#                     req_info["Strategy"],
#                     req_info["Pair"],
#                     req_info["Last Update"],
#                     req_info["Hold Time"],
#                     req_info["Last Rtn"],
#                     req_info["Last Rtn %"],
#                 ]
#             ]
#             returns_by_trade_df = concat(
#                 [returns_by_trade_df, DataFrame(trade_data, columns=returns_by_trade_df.columns)]
#             )
#             returns_by_trade_df.to_csv(returns_by_trade_path, index=False)
#     except Exception:
#         print_exc()
