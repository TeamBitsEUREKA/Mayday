import torchaudio
import numpy as np
from pydub import AudioSegment
from tortoise.utils.audio import load_voice
import soundfile as sf
import torch
from playsound import playsound
import os
import pyaudio
import wave
from pydub.playback import play
import simpleaudio as sa
from multiprocessing import Process
def play_audio(audio_data):
    audio_data *= 32767 / np.max(np.abs(audio_data))
    audio_data = audio_data.astype(np.int16)
    play_obj = sa.play_buffer(audio_data, 1, 2, 24000)
    play_obj.wait_done()


def talk(text, preset, voice, tts):
    def split_text(text):
        sentences = text.split('. ')
        return sentences

    sentences = split_text(text)

    # Initialize an instance of TextToSpeech
    

    voice_samples, conditioning_latents = load_voice(voice)

    # Initialize an empty AudioSegment
    full_audio = AudioSegment.empty()

    for idx, sentence in enumerate(sentences):
        # Generate the audio for this subdivision of text
        gen = tts.tts_with_preset(sentence, voice_samples=voice_samples, 
                                  conditioning_latents=conditioning_latents, preset=preset)
        audio_data = gen.squeeze(0).cpu().numpy()
        audio_data = audio_data / np.max(np.abs(audio_data))
        torchaudio.save(f'temp-{idx}.wav', torch.from_numpy(audio_data), 24000)


        # Save the generated audio to a temporary file
        temp_filename = f'temp-{idx}.wav'

        play_audio(audio_data)
        

        # Load the temporary file as an AudioSegment
        audio_segment = AudioSegment.from_wav(temp_filename)



        # Append the audio segment to the full_audio AudioSegment
        full_audio += audio_segment
        

    # Save the full_audio AudioSegment as a .wav file
    full_audio.export(f'generated-{voice}.wav', format="wav")

if __name__ == "__main__":
    text = "doing it right now." 
    preset = "ultra_fast"
    voice = 'demo_voice'
    talk(text, preset, voice)