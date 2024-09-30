import os
import random
from transformers import AutoModelForSequenceToSequenceLM, AutoTokenizer

# Load the AI model and tokenizer
model = AutoModelForSequenceToSequenceLM.from_pretrained("java-code-generator")
tokenizer = AutoTokenizer.from_pretrained("java-code-generator")

class JavaGenius:
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
        print(f"File created: {file_path}")

if __name__ == "__main__":
    javagenius = JavaGenius()
    file_type = input("Enter the file type (e.g. java, interface, enum): ")
    class_name = input("Enter the class name: ")
    package_name = input("Enter the package name: ")
    javagenius.create_file(file_type, class_name, package_name)
