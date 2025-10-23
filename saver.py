
# 保存
import time

def save_text(outputmoji: str) -> str:
    # 名称
    ts = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{ts}_transcript.txt"
    # 追記
    with open(filename, "a", encoding="utf-8") as f:
        f.write(outputmoji + "\n")
    # 戻り値
    return filename

