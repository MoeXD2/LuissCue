import docx
import whisper
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from moviepy.editor import *
from transformers import WhisperProcessor


ALLOWED_EXTENSIONS = {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}

def allowed_file(filename):
   return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXT = {'docx', 'pdf'}

# Check if the uploaded file has an allowed extension
def allowed_note(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def create_documents(transcription):
   with open('static/transcription.txt', 'w', encoding = "utf-8") as f:
      f.write(transcription)
   
   # Create a Word document
   doc = docx.Document()
   doc.add_paragraph(transcription)
   doc.save('static/transcription.docx')

   doc = SimpleDocTemplate('static/transcription.pdf', pagesize = letter)
   styles = getSampleStyleSheet()
   flowables = []

   # Wrap the text into a Paragraph
   transcription_paragraph = Paragraph(transcription, styles['Normal'])
   flowables.append(transcription_paragraph)

   # Add space between paragraphs (if you have multiple paragraphs)
   flowables.append(Spacer(1, 12))

   # Save the PDF
   doc.build(flowables)
   

def video_to_audio(video_path, audio_path):
   video_clip = VideoFileClip(video_path)
   audio_clip = video_clip.audio
   audio_clip.write_audiofile(audio_path)
   

def transcribe_file(file_path):
   model = whisper.load_model("base")
   processor = WhisperProcessor.from_pretrained("openai/whisper-small")
   sample_rate = processor.feature_extractor.sampling_rate

   audio = whisper.load_audio(file_path)
   audio_duration = len(audio) / sample_rate
   chunk_duration = 30  # seconds
   num_chunks = int(np.ceil(audio_duration / chunk_duration))

   full_transcription = ""
   for i in range(num_chunks):
      start_sample = i * chunk_duration * sample_rate
      end_sample = (i + 1) * chunk_duration * sample_rate
      audio_chunk = audio[start_sample:end_sample]
      audio_chunk = whisper.pad_or_trim(audio_chunk)

      mel = whisper.log_mel_spectrogram(audio_chunk).to(model.device)
      _, probs = model.detect_language(mel)
      detected_language = max(probs, key = probs.get)

      options = whisper.DecodingOptions(fp16 = False)
      result = whisper.decode(model, mel, options)
      full_transcription += result.text + " "

   return {'text': full_transcription, 'language': detected_language}