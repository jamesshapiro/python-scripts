import os

def concatenate_files(target_directory, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for root, dirs, files in os.walk(target_directory):
            for file in files:
                if not file.endswith('.js'):
                    continue
                if not 'src' in os.path.join(root, file):
                    continue
                if 'parcel' in os.path.join(root, file):
                    continue
                if 'node_modules' in os.path.join(root, file):
                    continue
                file_path = os.path.join(root, file)  
                output_file.write(f"```{file_path}\n")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_contents = f.read()
                    output_file.write(f"[{file_contents}]\n```\n\n")

# Example usage:
target_directory = '.'
output_file_path = './gemini-output.txt'
concatenate_files(target_directory, output_file_path)