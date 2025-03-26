# Importing required library
from googletrans import Translator

# Translate the text
class TranslateText:
    try:
        async def translate_text(self, source_text, targetLanguage, sourceLanguage):
            # Translator method for translation
            translator = Translator()

            # Source and target languages
            # if source_lang in googletrans.LANGUAGES
            if sourceLanguage == "sourceLanguage" and targetLanguage == "target_language":
                from_lang = 'hi'
                to_lang = 'en'
            elif sourceLanguage == "sourceLanguage" and targetLanguage != "target_language":
                from_lang = 'hi'
                to_lang = targetLanguage
            elif sourceLanguage != "sourceLanguage" and targetLanguage == "target_language":
                from_lang = sourceLanguage
                to_lang = 'en'
            else:
                from_lang = sourceLanguage
                to_lang = targetLanguage
            
            async with Translator() as translator:
                result = await translator.translate(source_text, src=from_lang, dest=to_lang)
                return result.text
    except Exception as e:
        print(f" Error while translating! {e}")
