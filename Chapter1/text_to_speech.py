from openai import OpenAI
import io
import sounddevice as sd
import soundfile as sf

client = OpenAI()


def text_to_speech(text):
    # 音声合成する
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
    )

    # 音声データを取得
    audio_buffer = io.BytesIO(response.content)

    # 音声データを読み込む（sig: 信号, sr: サンプリングレート）
    sig, sr = sf.read(audio_buffer)

    # 音声データを再生
    sd.play(sig, sr)
    sd.wait()


if __name__ == "__main__":
    # 音声に変換したいテキスト
    text1 = "私は音声対話型チャットボットです。"
    text2 = "なにかお手伝いできることはありますか？"

    text_to_speech(text1)
    text_to_speech(text2)
