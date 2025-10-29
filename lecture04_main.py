# lecture04_main.py

import os
import subprocess
from typing import List

# 必要なモジュールのインポート
# ただし、mainスクリプトで直接利用するのはtranscriberとsaverの関数のみ
# record.pyはsubprocessで実行する形を想定します (FFmpegの実行のため)
from transcriber import run_transcription_and_get_outputmoji
from saver import save_texts


# --- 設定 ---
AUDIO_FILE = "voice.wav"  # 録音ファイル名
# 録音時間 (record.pyの内容に合わせる)
# record.pyのduration変数の値を直接取得できないため、ここではハードコード (10秒)
RECORD_DURATION = 10 


def run_record() -> bool:
    """
    record.pyを実行して音声を録音します。
    
    Returns:
        bool: 録音に成功した場合はTrue、失敗した場合はFalse。
    """
    print(f"{RECORD_DURATION}秒間の録音を開始します...")
    # record.pyをサブプロセスとして実行
    try:
        # Popenを使って外部プロセスとして実行し、標準出力を表示
        process = subprocess.Popen(
            ["python", "record.py"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        # リアルタイムで出力を表示
        for line in process.stdout:
            print(line, end="")
        
        process.wait() # プロセスの終了を待機
        
        if process.returncode == 0:
            if os.path.exists(AUDIO_FILE):
                print(f"録音完了: {AUDIO_FILE} に保存されました。")
                return True
            else:
                print(f"録音は終了しましたが、ファイル '{AUDIO_FILE}' が見つかりません。")
                return False
        else:
            print(f"録音プロセスがエラーコード {process.returncode} で終了しました。")
            return False
            
    except FileNotFoundError:
        print("エラー: pythonコマンドが見つかりません。パスが設定されているか確認してください。")
        return False
    except Exception as e:
        print(f"録音処理中に予期せぬエラーが発生しました: {e}")
        return False


def run_transcription() -> List[str]:
    """
    transcriber.pyの機能を使って文字起こしを実行します。
    
    Returns:
        List[str]: 文字起こしの結果のリスト。エラーの場合は空のリスト。
    """
    print(f"\n'{AUDIO_FILE}' の文字起こしを開始します...")
    try:
        outputmoji = run_transcription_and_get_outputmoji(AUDIO_FILE)
        print("文字起こしが完了しました。")
        return outputmoji
    except FileNotFoundError:
        print(f"エラー: 音声ファイル '{AUDIO_FILE}' が見つかりません。録音が成功したか確認してください。")
        return []
    except Exception as e:
        print(f"文字起こし処理中にエラーが発生しました: {e}")
        return []


def run_saver(outputmoji: List[str]):
    """
    saver.pyの機能を使って文字起こし結果をファイルに保存します。
    
    Args:
        outputmoji (List[str]): 保存する文字起こし結果のリスト。
    """
    print("\n文字起こし結果をファイルに保存します...")
    saved_filename = save_texts(outputmoji)
    
    if saved_filename:
        print(f"保存完了: 結果は '{saved_filename}' に出力されました。")
    else:
        print("ファイル保存に失敗しました。")


def main():
    """
    すべての機能を順番に実行するメイン関数。
    """
    print("--- 🗣️ 文字起こし処理メインプログラムを開始します 📝 ---")
    
    # 1. 録音の実行
    if not run_record():
        print("\n--- 処理を終了します (録音失敗) ---")
        return
    
    # 2. 文字起こしの実行
    outputmoji = run_transcription()
    
    if not outputmoji:
        print("\n--- 処理を終了します (文字起こし失敗または結果なし) ---")
        return

    # 3. 結果の表示
    print("\n--- 文字起こし結果の確認 ---")
    for i, text in enumerate(outputmoji):
        print(f"[結果{i+1}] {text if text else '(空の文字列)'}")
        
    # 4. 結果の保存
    run_saver(outputmoji)
    
    print("\n--- 完了 ---")


if __name__ == "__main__":
    # 実行前に必要なファイルが存在するかチェック (簡略化のため、ここでは省略)
    # 実行環境によっては、'record.py' のFFmpeg入力デバイス設定('avfoundation', ':0')を
    # Windows/Linux向けに修正する必要があることに注意
    main()