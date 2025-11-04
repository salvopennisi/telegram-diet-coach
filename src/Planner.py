import requests, json
import os
from Utilities.output_messages_formatter import format_plan_for_telegram



def get_daily_plan(url, week_day_number=None, meal=None, logger=None):
    payload = json.dumps({"weekDayNumber": week_day_number, "meal": meal})
    params = {
        "action": "getPlan",
        "payload": payload
    }
    res = requests.get(url, params=params)
    if logger:
        logger.info(res)
    res.close()
    return format_plan_for_telegram(res.json())


