from flask import Flask, render_template, url_for, redirect, request, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from askpdf import process_user_query
from utils import allowed_file, create_documents, transcribe_file, video_to_audio, allowed_note
import os


# ------------------------------- Setup -------------------------------------------- #

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
NOTES_FOLDER = 'uploaded_notes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['NOTES_FOLDER'] = NOTES_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------------- #


@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/lessons')
def lessons():
   return render_template('lessons.html')

# ----------------------------- Notes Page -------------------------------------------- #

# Define the Note model
class Note(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(120), nullable = False)
   extension = db.Column(db.String(5), nullable = False)
   url = db.Column(db.String(255), nullable = False)

   def __repr__(self):
      return f'<Note {self.name}>'

# Route to render the notes page
@app.route('/notes')
def notes():
   db.create_all()
   notes = Note.query.all()
   return render_template('notes.html', notes = notes)

# Route to upload notes
@app.route('/upload_notes', methods = ['POST'])
def upload_notes():
   if request.method == 'POST':
      if 'file' not in request.files:
         return redirect(request.url)

      file = request.files['file']
      if file.filename == '':
         return redirect(request.url)

      if file and allowed_note(file.filename):
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['NOTES_FOLDER'], filename))
         extension = filename.rsplit('.', 1)[1].lower()
         url = os.path.join(app.config['NOTES_FOLDER'], filename)

         note = Note(name = filename, extension = extension, url = url)
         db.session.add(note)
         db.session.commit()

      return redirect(url_for('notes'))


# Route to delete a note
@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
   note = Note.query.get_or_404(note_id)
   db.session.delete(note)
   db.session.commit()

   # Optionally delete the file from the file system
   try:
      os.remove(os.path.join(app.config['NOTES_FOLDER'], note.name))
   except FileNotFoundError:
      pass
   
   return redirect(url_for('notes'))

# ---------------------------------- Transcribe Section--------------------------------------- #


@app.route('/transcribe', methods = ['POST'])
def transcribe():
   if 'file' not in request.files:
      return redirect(url_for('lessons'))

   file = request.files['file']
   if file.filename == '':
      return redirect(url_for('lessons'))

   if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(filepath)
      
      # Convert video to audio if the uploaded file is a video
      file_ext = filename.rsplit('.', 1)[1].lower()
      if file_ext in {'mp4', 'webm', 'mov'}:
         audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}_audio.wav')
         video_to_audio(filepath, audio_filepath)
         transcription_data = transcribe_file(audio_filepath)
         try:
            os.remove(audio_filepath)  # Remove the audio file after transcription
         except FileNotFoundError:
            pass
      else:
         transcription_data = transcribe_file(filepath)
      
      try:
         os.remove(filepath)  # Remove the audio file after transcription
      except FileNotFoundError:
         pass
         
      transcription = transcription_data['text']
      detected_language = transcription_data['language']
      create_documents(transcription)
      return render_template('lessons.html', transcription = transcription, detected_language = detected_language)

   return redirect(url_for('lessons'))


@app.route('/ask_question', methods = ['POST'])
def ask_question():
   question = request.json['question']
   text_file = "static/transcription.txt"
   llm_response = process_user_query(query = question, text_file = text_file)
   return jsonify({'answer': llm_response})


@app.route('/ask_note', methods = ['POST'])
def ask_note():
   note_id = request.json['note_id']
   question = request.json['question']
   
   note = Note.query.get_or_404(note_id)

   # Pass the note file path to the process_user_query function
   llm_response = process_user_query(query = question, text_file = note.url)

   return jsonify({'answer': llm_response})

# ----------------------------------------------------------------------------------- #

if __name__ == '__main__':
   app.run(debug = True)
