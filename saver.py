import time  # 時刻

def save_texts(outputmoji):
    # 名称
    filename = time.strftime("%Y%m%d_%H%M%S") + "_transcript.txt"
    try:
        # 書込み
        with open(filename, "w", encoding="utf-8") as f:
            if isinstance(outputmoji, list):
                for s in outputmoji:
                    f.write((s or "") + "\n")
            else:
                f.write(str(outputmoji) + "\n")
        # 完了
        print("--- 出力完了 ---")
        return filename
    except FileNotFoundError:
        # 例外
        print("エラー: ファイルなし")
        return ""
    except Exception as e:
        # 例外
        print(f"エラー: {e}")
        return ""

