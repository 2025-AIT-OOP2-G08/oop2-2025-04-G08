# 保存
import csv

def save_text(outputmoji: str, filepath: str = "recognized_text.csv") -> None:
    # 追記
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([outputmoji])
