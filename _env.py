import os
from typing import Tuple

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise KeyError("No TOKEN found!")

PRODUCTION_MODE = bool(os.environ.get('TELEGRAM_BOT_PRODUCTION', default=False))

def get_webhook_info() -> Tuple[str, int]:
    url = os.environ.get('URL')
    port = int(os.environ.get('PORT', 8000))
    return url, port