import os
import random
from transformers import AutoModelForSequenceToSequenceLM, AutoTokenizer
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

# Load the AI model and tokenizer
model = AutoModelForSequenceToSequenceLM.from_pretrained("java-code-generator")
tokenizer = AutoTokenizer.from_pretrained("java-code-generator")

class JavaJim:
    def __init__(self):
        self.model = model
        self.tokenizer = tokenizer

    def generate_java_code(self, file_type, class_name, package_name):
        # Generate the Java code using the AI model
        input_text = f"Generate {file_type} {class_name} in package {package_name}"
        inputs = self.tokenizer.encode_plus(input_text, 
                                            add_special_tokens=True, 
                                            max_length=512, 
                                            return_attention_mask=True, 
                                            return_tensors='pt')
        outputs = self.model(inputs['input_ids'], attention_mask=inputs['attention_mask'])
        generated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Create the file and write the generated code
        file_path = os.path.join(package_name.replace('.', '/'), f"{class_name}.{file_type}")
        with open(file_path, 'w') as f:
            f.write(generated_code)

        return file_path

    def create_file(self, file_type, class_name, package_name):
        # Create the file and write the generated code
        file_path = self.generate_java_code(file_type, class_name, package_name)
        return file_path

    def generate_video_game(self, game_name):
        # Generate the video game in Java
        input_text = f"Generate video game {game_name} in Java"
        inputs = self.tokenizer.encode_plus(input_text, 
                                            add_special_tokens=True, 
                                            max_length=512, 
                                            return_attention_mask=True, 
                                            return_tensors='pt')
        outputs = self.model(inputs['input_ids'], attention_mask=inputs['attention_mask'])
        generated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Create the jar file and batch file
        jar_file_path = os.path.join('games', f"{game_name}.jar")
        batch_file_path = os.path.join('games', f"{game_name}.bat")
        with open(jar_file_path, 'wb') as f:
            f.write(generated_code.encode('utf-8'))
        with open(batch_file_path, 'w') as f:
            f.write(f"java -jar {game_name}.jar")

        return jar_file_path, batch_file_path

class CodeForm(FlaskForm):
    file_type = StringField('File Type', validators=[DataRequired()])
    class_name = StringField('Class Name', validators=[DataRequired()])
    package_name = StringField('Package Name', validators=[DataRequired()])
    submit = SubmitField('Generate Code')

class GameForm(FlaskForm):
    game_name = StringField('Game Name', validators=[DataRequired()])
    submit = SubmitField('Generate Game')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CodeForm()
    if form.validate_on_submit():
        file_type = form.file_type.data
        class_name = form.class_name.data
        package_name = form.package_name.data
        javajim = JavaJim()
        file_path = javajim.create_file(file_type, class_name, package_name)
        return render_template('result.html', file_path=file_path)
    return render_template('index.html', form=form)

@app.route('/game', methods=['GET', 'POST'])
def game():
    form = GameForm()
    if form.validate_on_submit():
        game_name = form.game_name.data
        javajim = JavaJim()
        jar_file_path, batch_file_path = javajim.generate_video_game(game_name)
        return render_template('game_result.html', jar_file_path=jar_file_path, batch_file_path=batch_file_path)
    return render_template('game.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
