from process import text_toaudio, create_reell
from flask import Flask, render_template, request
import uuid
import os
from werkzeug.utils import secure_filename

# Create an absolute upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    reels_folder = os.path.join('static', 'reels')  # or your actual path
    videos = [f for f in os.listdir(reels_folder) if f.endswith('.mp4')]
    return render_template('index.html', videos=videos)
    # return render_template('index.html')

@app.route('/create-reel', methods=["GET", "POST"])
def create_reel():
    if request.method == "POST":
        rec_id = request.form.get("myid")
        if not rec_id:
            return "Error: myid is missing", 400

        text = request.form.get("prompt")
        files = request.files.getlist('photos')

        # Create upload directory for this rec_id
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        os.makedirs(upload_path, exist_ok=True)

        input_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_path, filename)
                file.save(file_path)
                input_files.append(filename)
        
        if not input_files:
            return "Error: No valid images uploaded.", 400

        # Save text and create FFmpeg input.txt
        text_file_path = os.path.join(upload_path, "text.txt")
        with open(text_file_path, "w") as fl:
            fl.write(text)

        ffmpeg_input_path = os.path.join(upload_path, "input.txt")
        with open(ffmpeg_input_path, "w") as f:
            for fl in input_files:
                f.write(f"file '{fl}'\nduration 1\n") # Use single quotes for filenames

        # Generate audio and reel
        try:
            audio_path = text_toaudio(text, rec_id)
            create_reell(rec_id, audio_path)
        except Exception as e:
            return f"Error during reel creation: {e}", 500

        # return f"Reel created successfully! Check folder: {upload_path}"

    # For GET request
    myid = uuid.uuid4()
    return render_template('create_reel.html', myid=myid)

@app.route('/gallery')
def gallery():
    videos = os.listdir("static/reels")  # All video filenames
    return render_template('gallery.html', videos=videos)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)