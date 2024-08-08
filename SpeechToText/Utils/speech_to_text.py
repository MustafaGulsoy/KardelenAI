import whisper
import base64
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'Commons', 'Models', 'TextToSpeech')
model = whisper.load_model("small", download_root=MODEL_PATH)


def test(base64_token):
    binary_data = base64.b64decode(base64_token)

    output_file_path = 'output.mp3'
    with open(output_file_path, 'wb') as binary_file:
        binary_file.write(binary_data)

        audio = whisper.load_audio(output_file_path)
        return model.transcribe(audio)
