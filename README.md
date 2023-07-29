# LuissCue
Transcribe and talk to your lessons and notes.

---

LuissCue is a Flask web app designed to help students study more effectively. It provides a platform for uploading and talking to notes, and transcribing and talking to lessons. The web app leverages OpenAI technologies to transcribe and summarize video / audio content, making it a powerful study aid for students.

### Features
**Notes**: Upload notes from and talk to them to enhance your learning experience.

**Lessons**: Explore lessons with AI-generated transcriptions and summaries for easy review and understanding.

**OpenAI Whisper**: Automatic Speech Recognition (ASR) system for transcribing video content.

**OpenAI Models**: Advanced AI models for summarizing transcribed text, providing concise and relevant summaries of video content.

### Getting Started
These instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites
```
Python 3.8 or higher
Flask
Tailwind CSS
Pytorch
Chocolatey
```

After installing Chocolatey, run the following command to install ffmpeg
```
choco install ffmpeg
```

### Installation

Clone the repository
```
git clone https://github.com/MoeXD2/LuissCue.git 
```
Change the current directory to the project directory
```
cd LuissCue
```
Create a virtual environment
```
python -m venv venv
```
Activate the virtual environment
On Windows:
```
venv\Scripts\activate
```
On macOS and Linux:
```
source venv/bin/activate
```
Install the required packages
```
pip install -r requirements.txt
```
Running the Application
Start the Flask development server
```
python app.py
```
Visit http://127.0.0.1:5000/ in your web browser to view the application.

ChromaDB for the open source vector database

Langchain for streamlining the development of diverse applications, such as chatbots, Generative Question-Answering (GQA), and summarization
