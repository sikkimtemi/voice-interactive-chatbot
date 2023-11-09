import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
import numpy as np
import threading
import time

client = OpenAI()

# 録音のパラメータ
fs = 44100  # サンプルレート
recording = np.array([])  # 録音データを保存する配列

# 録音の開始と終了を制御するフラグ
is_recording = False


def record():
    """録音する関数"""
    global is_recording
    global recording
    while True:
        if is_recording:
            # 録音中の場合、0.5秒分の録音データを追加
            recording_chunk = sd.rec(int(0.5 * fs), samplerate=fs, channels=1)
            sd.wait()
            recording = np.append(recording, recording_chunk)
        else:
            # CPU負荷を下げるために1ミリ秒待機
            time.sleep(0.001)


# 録音スレッドの開始
recording_thread = threading.Thread(target=record)
recording_thread.start()


def speech_to_text():
    """音声認識する関数"""
    global is_recording
    global recording
    input("Enterキーを押すと録音を開始します。\n")
    # 録音を開始
    is_recording = True
    print("録音を開始します。\n")
    input("録音中です。Enterを押すと録音を終了します。\n")
    # 録音を終了
    is_recording = False
    print("録音が終了しました。")
    if recording.size > 0:
        # 録音データが存在する場合、データをファイルに保存
        write("output.wav", fs, recording)

        # ファイルをバイナリモードで開く
        with open("output.wav", "rb") as audio_file:
            # Transcriptions APIを呼び出して音声認識する
            transcript = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, language="ja"
            )

        # 録音データをリセット
        recording = np.array([])

        # 音声認識結果を返す
        return transcript.text


if __name__ == "__main__":
    while True:
        text = speech_to_text()
        print("\n音声認識結果: {}\n".format(text))
