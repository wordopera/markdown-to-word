import sys
import os
from datetime import datetime
from markdown_parser import MarkdownParser
from word_generator import WordGenerator

def convert_markdown_to_word(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        parser = MarkdownParser()
        elements = parser.parse(markdown_text)

        generator = WordGenerator()
        generator.generate(elements)
        generator.save(output_file)
        return True
    except Exception as e:
        print(f"Error converting {input_file}: {str(e)}")
        return False

if __name__ == "__main__":
    input_folder = os.path.join(os.path.dirname(__file__), '..', 'input')
    output_folder = os.path.join(os.path.dirname(__file__), '..', 'output')
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    successful_conversions = 0
    total_files = 0
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.md'):
            total_files += 1
            input_file = os.path.join(input_folder, filename)
            timestamp = datetime.now().strftime('%M%S')
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_{timestamp}.docx")
            
            if convert_markdown_to_word(input_file, output_file):
                successful_conversions += 1
                print(f"Converted {filename} to {os.path.basename(output_file)}")
            
    print(f"\nConversion complete. Successfully converted {successful_conversions} out of {total_files} files.")