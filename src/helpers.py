from datetime import datetime


def system_msg(msg: str) -> None:
    print(f"[{datetime.now().isoformat()}] {msg}")
