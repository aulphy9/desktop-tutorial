import os
import subprocess

def run_code_file(code_file, input_file):
    # Determine the file type
    file_extension = os.path.splitext(code_file)[1].lower()

    if file_extension == ".py":
        # Run Python code file
        command = f"python {code_file} < {input_file}"
    elif file_extension == ".java":
        # Compile and run Java code file
        class_name = os.path.splitext(os.path.basename(code_file))[0]
        source_directory = os.path.dirname(code_file)
        class_file = os.path.join(source_directory, f"{class_name}.class")

        # Compile the Java code explicitly
        subprocess.run(["javac", code_file], check=True)

        # Run the Java code file
        process = subprocess.Popen(["java", "-cp", source_directory, class_name+".java"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open(input_file, 'r') as f:
            output, error = process.communicate(input=f.read().encode())
        output = output.decode().strip()
    else:
        print(f"Unsupported file type: {file_extension}")
        return None

    return output

def compare_output(output, expected_output_file):
    with open(expected_output_file, 'r') as f:
        expected_output = f.readlines()

    output_lines = output.strip().split('\n')
    num_expected_lines = len(expected_output)
    num_output_lines = len(output_lines)
    num_correct_lines = 0

    for i in range(min(num_expected_lines, num_output_lines)):
        if output_lines[i].strip() == expected_output[i].strip():
            num_correct_lines += 1

    correctness_percentage = (num_correct_lines / num_expected_lines) * 100
    return correctness_percentage

def evaluate_project(project_path, input_folder, expected_output_folder):
    src_path = os.path.join(project_path, "src\\cp213")

    for root, _, files in os.walk(src_path):
        for file in files:
            code_file = os.path.join(root, file)
            expected_output_file = os.path.join(expected_output_folder, file.replace('.py', '.txt').replace('.java', '.txt'))

            if os.path.isfile(expected_output_file):
                input_file = os.path.join(input_folder, file.replace('.py', '.txt').replace('.java', '.txt'))
                if os.path.isfile(input_file):
                    with open(input_file, 'r') as f:
                        input_lines = f.readlines()

                    for input_line in input_lines:
                        output = run_code_file(code_file, input_file)
                        if output is not None:
                            mark = compare_output(output, expected_output_file)
                            print(f"{file} - Input: {input_line.strip()} - Mark: {mark}%")

def main():
    project_folder = "autograder\\test_code_files"
    input_folder = "autograder\\test_input_files"
    expected_output_folder = "autograder\\test_output_files"

    for project in os.listdir(project_folder):
        project_path = os.path.join(project_folder, project)
        if os.path.isdir(project_path):
            evaluate_project(project_path, input_folder, expected_output_folder)

if __name__ == "__main__":
    main()
