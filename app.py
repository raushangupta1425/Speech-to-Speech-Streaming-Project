# Import required libraries
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
import yt_dlp
import asyncio
from custom_api.translate_text import TranslateText

# Import custom APIs libraries
from custom_api.extract_audio import ExtractAudioFromVideo
from custom_api.audio_to_text import AudioTranscriber
from custom_api.text_to_speech import TextToSpeech
from custom_api.merge_video_with_speech import MergeVideoAudio
from custom_api.correct_text import CorrectText

app = Flask(__name__)

@app.route('/dubbed_videos/<path:filename>')
def dubbed_videos(filename):
    return send_from_directory('dubbed_videos', filename)

@app.route('/')
def home():
    return render_template('index.html')

UPLOAD_FOLDER = 'uploads'  # adjust according to your project structure
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        video_url = url_for('uploaded_file', filename=filename)
        return jsonify({
            'message': 'Video uploaded successfully.',
            'filename': filename,
            'video_url': video_url
        })
    else:
        return jsonify({'message': 'No file uploaded'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form.get("link")
        current_folder = os.path.dirname(os.path.abspath(__file__))
        output_path = current_folder+"/downloads/"

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",  # Forces MP4 format
            "merge_output_format": "mp4",  # Ensures final output is MP4
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'message': 'Download successfully!'})
    except Exception as e:
        return jsonify({'message': 'File already exist!'})


@app.route('/start', methods=['POST'])
def start():
    filenameWithExtension = request.form.get('video')
    videoPath = './uploads/' + filenameWithExtension
    # Step 1
    extract = ExtractAudioFromVideo()
    original_video_path = videoPath
    extractedAudioFileName = extract.extract_audio(original_video_path)

    # Step 2
    generated_text = AudioTranscriber().get_large_audio_transcription_on_silence(extractedAudioFileName)
    return jsonify({'message': 'Text transcribe successfully!', 'text': generated_text, 'filenameWithExtension': filenameWithExtension, 'original_video_path': original_video_path})

@app.route('/translate', methods=['POST'])
def translate():
    # Step 3
    try:
        # Get data from the request
        generated_text = request.form.get('generatedText')
        target_language = request.form.get('targetLanguage')
        source_language = request.form.get('sourceLanguage')

        if not generated_text or not target_language or not source_language:
            return jsonify({'message': 'Missing required fields'}), 400

        # Assuming TranslateText().translate_text() is an async function
        translated_text = CorrectText.correct_text(generated_text, target_language, source_language)
        # translated_text = asyncio.run(TranslateText().translate_text(generated_text, target_language, source_language))

        return jsonify({'message': 'Text translated successfully!', 'text': translated_text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error translating text', 'error': str(e)}), 500
    

@app.route('/finish', methods=['POST'])
def finish():
    try:
        # Retrieve form data
        translated_text = request.form.get('translatedText')
        filename_with_extension = request.form.get('filenameWithExtension')
        original_video_path = request.form.get('original_video_path')

        if not translated_text or not filename_with_extension or not original_video_path:
            return jsonify({'message': 'Missing required fields'}), 400

        # Step 4: Convert text to speech
        audio_file_name = TextToSpeech().text_to_speech(translated_text)  # Ensure this function returns a valid filename

        # Step 5: Prepare video filename
        filename_without_extension, _ = os.path.splitext(filename_with_extension)  # Extract filename without extension
        dubbed_video_path = f"{filename_without_extension}"  # Define the final dubbed file path

        # Merge video with new audio
        merger = MergeVideoAudio()
        dubbed_video_filename = merger.merge_audio_with_video(original_video_path, audio_file_name, dubbed_video_path)

        # Generate URL for the dubbed video (Ensure the endpoint serves files correctly)
        dubbed_url = url_for('dubbed_videos', filename=dubbed_video_filename, _external=True)

        return jsonify({
            'message': 'Dubbing completed successfully.',
            'filename': dubbed_video_filename,
            'dubbed_url': dubbed_url
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error during dubbing process', 'error': str(e)}), 500

    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
