# SPEECH-TO-SPEECH-STREAMING_APP
This project help us to dubbed any video to our preference languages. If we have any video which is in another language,  which we can't able to understand then we can dubbed that video language into our understanding languages.

## Steps for completing project.
1. Audio extraction - ffmpeg package
2. Audio to text
3. text to translated text
4. text to audio
5. mergea audio with original video

## Prons
    - maximun video length upto 5 minutes till now

## Important Instruction before running app
    - Rename your video name as "video" to work properly

## Follow the instruction
1. Audio extraction : extract_audio.py  -  ffmpeg package
    - First, you have to download and setup its file in windows or any operating system that you have. For that, click on this link : https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z  the file will be downloaded for windows operating system. For any other operating system, click on this link : https://ffmpeg.org/download.html  then choose your operating system and download the file.

    - Second, Extract the downloaded file and move it in C drive and rename it as "ffmpeg" directory name.

    - Third, Open command prompt as Run as adminstration and type the command setx /m PATH "C:\ffmpeg\bin;%PATH%"  for setup environment variables

    - Fourth, Restart the pc
    
    - Fifth, then in vs terminal run this command "pip install ffmpeg-python" and follow the above code, Now you are ready to extract audios file from videos.
    
2. Audio to text : audio_to_text.py  - SpeechRecognition, pydub, os
    - Install these libraries SpeechRecognition, pydub
    - Follow the code above
    - You can also change the value of below variables to set more accuracy:
        - min_silence_len = 500, : 
            - This sets the minimum length of silence (in milliseconds) that the function should recognize as a "split point."
            - 500 means that any silence lasting half a second or more will be considered a boundary to split the audio into chunks.
            - If your audio has longer pauses, you can increase this value; for shorter pauses, decrease it.
        - silence_thresh = sound.dBFS-10, :
            - dBFS stands for "Decibels relative to Full Scale," which measures loudness.
            - sound.dBFS gives the average loudness of the entire audio.
            - By subtracting 14, you're setting the silence threshold to be 14 decibels lower than the average loudness.
            - Any part of the audio quieter than this threshold for at least min_silence_len milliseconds will be considered silence.
            - You can adjust -14 depending on how "quiet" the silence in your audio is. Larger negative values make it more sensitive.
        - keep_silence=500, :
            - This determines how much of the detected silence (in milliseconds) to keep at the beginning and end of each chunk.
            - In this example, it keeps 500 milliseconds (0.5 seconds) of silence padding at both ends of the split chunks.
            - This can make the resulting chunks sound more natural if you're planning to process or play them separately.
    - Call the function and text will be generated.

3. Text to Translated Text : translate_text.py  - googletrans
    - You can print all supported languages through this code "print(googletrans.LANGUAGES)"
    - from_lang = 'hi' provide language code of source text.
    - to_lang = 'en' provide language code of targeted text
    - Provide source text during function call as argument.

4. Text To Audio : text_to_speech.py  - edge_tts
    - You can choose your language from the listing voices and pass as parameter in lang 
    - You can choose your gender voice from the listing voices and pass as parameter in gender

5. Mergea audio with original video : merge_video_with_speech.py  - moviepy
    - You will get the output video with the name dubbed_video.mp4