# Import required libraries
from flask import Flask, render_template, request, jsonify

# Import custom APIs libraries
from custom_api.extract_audio import ExtractAudioFromVideo
from custom_api.audio_to_text import AudioTranscriber
from custom_api.text_to_speech import TextToSpeech
from custom_api.merge_video_with_speech import MergeVideoAudio

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    file.save(f"./uploads/{file.filename}")  # Save the file
    return jsonify({"message": "File saved", "filename": file.filename})

@app.route('/start', methods=['POST'])
def start():
    filenameWithExtension = request.form.get('video')
    videoPath = './uploads/' + filenameWithExtension
    # Step 1
    extract = ExtractAudioFromVideo()
    original_video_path = videoPath
    extractedAudioFileName = extract.extract_audio(original_video_path)

    # Step 2 and 3
    translated_text = AudioTranscriber().get_large_audio_transcription_on_silence(extractedAudioFileName)

    # Step 4
    audioFileName = TextToSpeech().text_to_speech(translated_text) # must give text as argument

    # Step 5
    filenameWithoutExtension = filenameWithExtension.split('.')
    dubbedVideoPath = filenameWithoutExtension[0]
    merger = MergeVideoAudio()
    merger.merge_audio_with_video(original_video_path, audioFileName, dubbedVideoPath)
    return jsonify({"message": "Dubbed successfully!"})

    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
