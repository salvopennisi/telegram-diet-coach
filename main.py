import requests, json
# import urllib.parse
# payload = urllib.parse.quote('{"weekDayNumber":1,"meal":"Colazione"}')
# print(payload)


GAS_BASE_URL = "https://script.google.com/macros/s/AKfycbxpi8eh0Rs1edtIJ7e_eoYdUgamzZjqM-yWbK5pSaMBmldWSmu1www2v34hSyKRtrpD/exec"

def format_plan_for_telegram(plan: dict) -> str:
    """
    Converte un dizionario del piano giornaliero (singolo pasto o più pasti)
    in un messaggio leggibile per Telegram con Markdown.
    """
    # Caso 1️⃣: più pasti (dizionario di dizionari)
    try:
        if any(isinstance(v, dict) for v in plan.values()):
            parts = []
            for meal, items in plan.items():
                meal_lines = [f"🍽️ *{meal}*"]
                for item, qty in items.items():
                    meal_lines.append(f"- {item}: {qty}g")
                parts.append("\n".join(meal_lines))
            return "\n\n".join(parts)

        # Caso 2️⃣: singolo pasto (dizionario piatto)
        else:
            lines = []
            for item, qty in plan.items():
                lines.append(f"- {item}: {qty}g")
            return "\n".join(lines)
    except:
        return json.dumps(plan)


def get_plan(week_day_number=None, meal=None):
    payload = json.dumps({"weekDayNumber": week_day_number, "meal": meal})
    params = {
        "action": "getPlan",
        "payload": payload
    }
    res = requests.get(GAS_BASE_URL, params=params)
    res.close()
    return format_plan_for_telegram(res.json())

# Esempio uso:
print(get_plan())
