import os

def crawl_and_print_files(start_path, output_file):
    output_file_path = os.path.join(start_path, output_file)  # Full path to the output file

    with open(output_file_path, 'w', encoding='utf-8') as f:
        # Heading for the output
        f.write("\nBelow is the complete source code for the project:\n")
        f.write("=" * 49 + "\n")

        for root, dirs, files in os.walk(start_path):
            files = [file for file in files if os.path.join(root, file) != output_file_path]  # Filter out the output file
            for file in files:
                file_path = os.path.join(root, file)
                f.write(f"\nFile: {file_path}\n\n")
                f.write("```\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as file_content:
                        f.write(file_content.read())
                except Exception as e:
                    f.write(f"Error reading file {file_path}: {e}\n")
                f.write("```\n")

        f.write("=" * 49 + "\n")

# Replace '.' with the directory you want to start from
crawl_and_print_files('.', 'flattened.txt')
