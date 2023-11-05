import requests
from playsound import playsound

# VOICEVOX EngineのURL
VOICEVOX_URL = "http://localhost:50021"

def text_to_speech(text):
    # 音声合成のためのクエリを生成
    response = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={
            "text": text,
            "speaker": 58,
        },
    )
    audio_query = response.json()

    # 音声合成を行う
    response = requests.post(
        f"{VOICEVOX_URL}/synthesis",
        headers={
            "Content-Type": "application/json",
        },
        params={
            "speaker": 58,
        },
        json=audio_query,
    )

    # ステータスコードが200以外の場合はエラーメッセージを表示
    if response.status_code != 200:
        print("エラーが発生しました。ステータスコード: {}".format(response.status_code))
        print(response.text)
    else:
        # 音声データを取得
        audio = response.content

        # 音声データをファイルに保存
        with open("output.wav", "wb") as f:
            f.write(audio)

        # 音声データを再生
        playsound("output.wav")

if __name__ == "__main__":
    # 音声に変換したいテキスト
    text = "かつおぶしが好きにゃ。"
    text_to_speech(text)
