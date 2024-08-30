from flask import Flask, request, redirect, url_for, render_template
import os
import whisper

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/' 

# Whisperモデルのロード
model = Whisper(model_name="base")

@app.route('/', methods=['POST', 'GET'])
def home():
    result_text = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)

        if file:
            # ファイルを一時的に保存
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Whisperモデルで音声ファイルを処理
            result = model.transcribe(filepath)

            # 認識結果を取得
            result_text = result['text']
            
            # 一時ファイルの削除
            os.remove(filepath)

    return render_template('index.html', text=result_text)
'''
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = file.filename 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully!'
    
    return redirect(request.url)
'''
if __name__ == '__main__':
    app.run(debug=True)
