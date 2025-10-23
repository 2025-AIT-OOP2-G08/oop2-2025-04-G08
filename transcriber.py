import mlx_whisper
from pydub import AudioSegment
import numpy as np
from typing import Dict, Any, List

def run_transcription_and_get_outputmoji(
    audio_file_path: str = "voice.wav", 
    model_name: str = "whisper-base-mlx"
) -> List[str]:
    
    # 文字起こし結果を格納する変数
    outputmoji: List[str] = []

    # --- 元のコードの「音声ファイルを指定して文字起こし」の部分 ---
    
    # 処理の実行
    result: Dict[str, Any] = mlx_whisper.transcribe(
      audio_file_path, path_or_hf_repo=model_name
    )
    # 結果のテキストを outputmoji に格納
    outputmoji.append(result.get("text", "").strip())
    
    # --- 元のコードの「音声データを指定して文字起こし」の部分 ---
    
    def preprocess_audio(sound):
        # この関数は元のコードの構造を保つため、内部に定義
        if sound.frame_rate != 16000:
            sound = sound.set_frame_rate(16000)
        if sound.sample_width != 2:
            sound = sound.set_sample_width(2)
        if sound.channels != 1:
            sound = sound.set_channels(1)
        return sound

    audio_data = []

    # 音声データを音声ファイルから読み取る
    # 元のコードで "voice.wav" を読み込んでいた処理
    audio_data.append(AudioSegment.from_file(audio_file_path, format="wav"))

    for data in audio_data:
        sound = preprocess_audio(data)
        # Metal(GPU)が扱えるNumpy Array形式に変換
        arr = np.array(sound.get_array_of_samples()).astype(np.float32) / 32768.0
        
        result_data: Dict[str, Any] = mlx_whisper.transcribe(
            arr, path_or_hf_repo=model_name
        )
        # 結果のテキストを outputmoji に格納
        outputmoji.append(result_data.get("text", "").strip())
        
    return outputmoji

if __name__ == '__main__':
    
    # テスト用のファイルパス
    INPUT_FILE = "voice.wav"
    
    try:
        # 関数を実行し、結果を outputmoji 変数に格納
        outputmoji = run_transcription_and_get_outputmoji(INPUT_FILE)
        
        print("--- 文字起こし処理が完了しました ---")
        print(f"次の人に渡す変数 outputmoji の内容:\n{outputmoji}")
        
    except FileNotFoundError:
        print(f"エラー: 音声ファイル {INPUT_FILE} が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")