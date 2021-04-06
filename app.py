from flask import Flask,flash, render_template,request
from text_cleaning import clean_string
from text_extraction import text_extraction
from text_summary import predict
import time
import spacy
nlp = spacy.load("en_core_web_sm")
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pickle
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = 'text-summary-web/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc'}

app = Flask(__name__)
file_name = "spacy_summary.pkl"
model = pickle.load(open(file_name,'rb'))

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




# def readingtime(mytext):
#     total_words = len([token.text for token in nlp(mytext)])
#     estimated_time = total_words/200.0
#     return estimated_time

#Text from url
def get_report(url):
    page = urlopen(url)
    soup = BeautifulSoup(page,"lxml")
    pull_text =' '.join(map(lambda p:p.text.soup.find_all('p')))
    return pull_text

@app.route('/',methods=["Get"])
def home():
    return render_template('home.html')

@app.route('/analyze_text',methods=['Post'])
def analyze_text():
    print("analyze_text")
    start = time.time()
    spacy_summary = ""
    final_time = None
    print(request.method)
    if request.method == 'POST':
        print("post")
        rawtext = request.form['rawtext']
        print(rawtext)
        #Text Processing
        clean = clean_string(rawtext)
        # reading_time = readingtime(clean)
        #Summarization
        spacy_summary = predict(clean,1)
        #Reading time
        # summary_reading_time = readingtime(spacy_summary)
        end = time.time()
        final_time = end-start
    return render_template('home.html',spacy_summary = spacy_summary)

@app.route('/analyze',methods=['Post'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('Invalid file format')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser but
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('Please select a file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return 
def analyze_pdf():
    if request.method =='POST':
        print("Post")
        filename = request.form['filename']
        start = time.time()
        #Extraction
        extraction = text_extraction(filename)
        #Text Processing  
        clean = clean_string(extraction)
        # reading_time = readingtime(clean)
        #Summarization
        spacy_summary_2 = predict(clean,1)
        #Reading time
        # summary_reading_time = readingtime(spacy_summary)
        end = time.time()
        final_time = end-start
        return render_template('home.html',spacy_summary_2 = spacy_summary_2)


@app.route('/analyze_url', methods=['Post'])
def analyze_url():
    start = time.time()
    raw_url = request.form['raw_url']
    raw_text = get_report(raw_url)
    #Text Processing
    clean = clean_string(raw_text)
    # reading_time = readingtime(clean)
    #Summarization
    spacy_summary_3 = predict(clean,1)
    #Reading time
    # summary_reading_time = readingtime(spacy_summary)
    end = time.time()
    final_time = end-start
    return render_template('home.html',spacy_summary_3 = spacy_summary_3)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
if __name__ == '__main__':
    app.run(debug=True)