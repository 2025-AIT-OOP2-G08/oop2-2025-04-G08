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

    # --- ファイルから直接文字起こし ---
    result: Dict[str, Any] = mlx_whisper.transcribe(
        audio_file_path, path_or_hf_repo=model_name
    )
    outputmoji.append(result.get("text", "").strip())

    # --- 音声データとして再度文字起こし ---
    def preprocess_audio(sound):
        if sound.frame_rate != 16000:
            sound = sound.set_frame_rate(16000)
        if sound.sample_width != 2:
            sound = sound.set_sample_width(2)
        if sound.channels != 1:
            sound = sound.set_channels(1)
        return sound

    audio_data = []
    audio_data.append(AudioSegment.from_file(audio_file_path, format="wav"))

    for data in audio_data:
        sound = preprocess_audio(data)
        arr = np.array(sound.get_array_of_samples()).astype(np.float32) / 32768.0
        result_data: Dict[str, Any] = mlx_whisper.transcribe(
            arr, path_or_hf_repo=model_name
        )
        outputmoji.append(result_data.get("text", "").strip())
        
    return outputmoji


# --- テスト実行用コード ---
if __name__ == "__main__":
    INPUT_FILE = "voice.wav"  # テストする音声ファイル名
    
    try:
        print(f"--- {INPUT_FILE} の文字起こしを開始します ---")
        outputmoji = run_transcription_and_get_outputmoji(INPUT_FILE)

        print("\n--- 文字起こしが完了しました ---")
        for i, text in enumerate(outputmoji):
            print(f"[結果{i+1}] {text if text else '(空の文字列)'}")

    except FileNotFoundError:
        print(f"エラー: 指定された音声ファイル '{INPUT_FILE}' が見つかりません。")
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")
