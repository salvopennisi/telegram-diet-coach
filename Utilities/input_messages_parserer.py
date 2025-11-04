from datetime import datetime

import re
from datetime import datetime

def parse_message_for_plan(text: str, logger=None):
    # Normalizza il testo
    original_text = text
    text = text.strip().lower()

    if logger:
        logger.info(f"Parsing messaggio utente: '{original_text}' → '{text}'")

    # Giorni della settimana (gestione accenti)
    giorni_patterns = {
        r"\bluned[ìi]?\b": 1,
        r"\bmarted[ìi]?\b": 2,
        r"\bmercoled[ìi]?\b": 3,
        r"\bgioved[ìi]?\b": 4,
        r"\bvenerd[ìi]?\b": 5,
        r"\bsabat[oa]?\b": 6,
        r"\bdomenic[ae]?\b": 7,
    }

    # Tutti i pasti (con regex flessibili per accenti e spazi)
    pasti_patterns = {
        r"\bcolazi?one\b": "Colazione",
        r"\bpranzo\b": "Pranzo",
        r"\bcen[ae]?\b": "Cena",
        r"\bspuntin[oi]?\b": "Spuntino",
        r"\bmerend[ae]?\b": "Merenda",
        r"\bpre[- ]?workout\b": "Pre-workout",
        r"\bpost[- ]?workout\b": "Post-workout",
    }

    week_day_number = None
    meal = None
    today = datetime.now().isoweekday()

    # 🔹 “oggi / ieri / domani”
    if re.search(r"\boggi\b", text):
        week_day_number = today
    elif re.search(r"\bier[iì]\b", text):
        week_day_number = today - 1 if today > 1 else 7
    elif re.search(r"\bdomani\b", text):
        week_day_number = today + 1 if today < 7 else 1

    # 🔹 Cerca giorno della settimana
    if week_day_number is None:
        for pattern, num in giorni_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                week_day_number = num
                break

    # 🔹 Cerca numero esplicito (es: “piano 3”)
    if week_day_number is None:
        match_num = re.search(r"\b([1-7])\b", text)
        if match_num:
            week_day_number = int(match_num.group(1))

    # 🔹 Cerca pasto
    for pattern, nome in pasti_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            meal = nome
            break

    # 🔹 Nessun match trovato
    if week_day_number is None and meal is None:
        if logger:
            logger.warning(f"Nessun giorno o pasto riconosciuto nel messaggio: '{text}'")
        raise ValueError("Nessun giorno o pasto riconosciuto nel messaggio")

    # 🔹 Default: se manca giorno → oggi
    if week_day_number is None:
        week_day_number = today

    if logger:
        logger.info(f"Interpretato → Giorno={week_day_number}, Pasto={meal}")

    return week_day_number, meal
