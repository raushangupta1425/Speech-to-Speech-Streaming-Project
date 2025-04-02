# Importing required libraries
import edge_tts
import asyncio

# Top most used voices
Voices = {
    "Spanish": {"male": "es-ES-AlvaroNeural", "female": "es-ES-ElviraNeural"},
    "French": {"male": "fr-FR-HenriNeural", "female": "fr-FR-DeniseNeural"},
    "German": {"male": "de-DE-ConradNeural", "female": "de-DE-KatjaNeural"},
    "Hindi": {"male": "hi-IN-MadhurNeural", "female": "hi-IN-SwaraNeural"},
    "Bhojpuri": {"male": "hi-IN-MadhurNeural", "female": "hi-IN-SwaraNeural"},  
    "Tamil": {"male": "ta-IN-ValluvarNeural", "female": "ta-IN-PallaviNeural"},
    "Gujarati": {"male": "gu-IN-NiranjanNeural", "female": "gu-IN-DhwaniNeural"},
    "Kannada": {"male": "kn-IN-GaganNeural", "female": "kn-IN-SapnaNeural"},
    "Korean": {"male": "ko-KR-InJoonNeural", "female": "ko-KR-SunHiNeural"},
    "Japanese": {"male": "ja-JP-KeitaNeural", "female": "ja-JP-NanamiNeural"},
    "Malayalam": {"male": "ml-IN-MidhunNeural", "female": "ml-IN-SobhanaNeural"},
    "Marathi": {"male": "mr-IN-ManoharNeural", "female": "mr-IN-SwaraNeural"},
    "Telugu": {"male": "te-IN-MohanNeural", "female": "te-IN-ShrutiNeural"},  
    "Arabic": {"male": "ar-SA-FareedNeural", "female": "ar-SA-ZariyahNeural"},
    "Bengali": {"male": "bn-IN-BashkarNeural", "female": "bn-IN-TanishaaNeural"},
    "Chinese": {"male": "zh-CN-YunxiNeural", "female": "zh-CN-XiaoxiaoNeural"},
    "Portuguese": {"male": "pt-PT-FernandoNeural", "female": "pt-PT-FernandaNeural"},
    "Russian": {"male": "ru-RU-DmitryNeural", "female": "ru-RU-SvetlanaNeural"},
    "English": {"male": "en-US-GuyNeural", "female": "en-US-JennyNeural"}
}

class ConvertIntoSpeech:
    def __init__(self):
        self.voices = Voices

    async def convert(self, mytext, tarLang="English", gender="male", output_file="translatedAudio.mp3"):
        print('Converting text to speech...')
        try:
            text = f"""{mytext}"""
            voice = self.voices[tarLang][gender.lower()]
            communicate = edge_tts.Communicate(text, voice, rate="-10%")  # Decrease speed by 10%
            await communicate.save(output_file)
            print(f"Speech saved as {output_file}")
            print('Text converted to speech successfully!')
            return output_file
        except Exception as e:
            print(f"Error while generating speech: {e}")
            return None

class TextToSpeech:
    def text_to_speech(self, translated_text, tarLang):
        audioFileName = asyncio.run(ConvertIntoSpeech().convert(translated_text, tarLang))
        return audioFileName