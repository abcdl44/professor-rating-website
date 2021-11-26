from datetime import datetime

# i kinda just stole this utils file, please don't sue

def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")
