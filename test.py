from tortoise.api import TextToSpeech
from tts import talk


def load_tts_model():
    global tts
    tts = TextToSpeech()
    return tts


def pass_value():
    return tts