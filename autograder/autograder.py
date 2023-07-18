import os

def run_code_file(code_file, input_line):
    # Determine the file type
    file_extension = os.path.splitext(code_file)[1].lower()


    class_name = os.path.splitext(os.path.basename(code_file))[0]

    if file_extension == ".py":
        original_dir=os.getcwd()
        # Run Python code file
        command = f"python {class_name}.py"
        #extract class directory
        class_dir=os.path.dirname(code_file)
        #set that to cd
        os.chdir(class_dir)
    elif file_extension == ".java":
        # Compile and run Java code file
        command = f"javac {code_file}"
        os.system(command)
        #keep original directory
        original_dir=os.getcwd()
        #extract class directory
        class_dir=os.path.dirname(code_file)
        #set that to cd
        os.chdir(class_dir)
        # Execute the command and capture the output
        command= f"java {class_name}"
    else:
        print(f"Unsupported file type: {file_extension}")
        return None
    
    with open("temp.txt", "w") as temp_file:
        temp_file.write(input_line)
    
    command +=f" < temp.txt"
    output = os.popen(command).read()

    os.remove("temp.txt")
    #switch back to original directory
    os.chdir(original_dir)


    return output

def compare_output(output, expected_output_file):
    with open(expected_output_file, 'r') as f:
        expected_output = [line for line in f.readlines() if line.strip()]

    output_lines = [line for line in output.strip().split('\n') if line.strip()]
    num_expected_lines = len(expected_output)
    num_output_lines = len(output_lines)
    num_correct_lines = 0

    for i in range(min(num_expected_lines, num_output_lines)):
        if output_lines[i].strip() == expected_output[i].strip():
            num_correct_lines += 1

    correctness_percentage = (num_correct_lines / num_expected_lines) * 100
    return correctness_percentage

def evaluate_project(project_path, input_file, expected_output_folder):
    src_path = os.path.join(project_path, "src")

    for root, _, files in os.walk(src_path):
        for file in files:
            code_file = os.path.join(root, file)
            expected_output_file = os.path.join(expected_output_folder, file.replace('.py', '.txt').replace('.java', '.txt'))

            if os.path.isfile(expected_output_file):
                output=''
                correctness_percentage=0
                with open(input_file, "r") as f:
                    for line in f:
                        temp = run_code_file(code_file, line)
                        if temp is not None:
                            output+=temp
                correctness_percentage = compare_output(output, expected_output_file)
                print(f"{file} - Correctness: {correctness_percentage:.2f}%")

def main():
    project_folder = "autograder\\test_code_files"
    input_file = "autograder\\test_input_files\\Palindrome.txt"
    expected_output_folder = "autograder\\test_output_files"

    for project in os.listdir(project_folder):
        project_path = os.path.join(project_folder, project)
        if os.path.isdir(project_path):
            evaluate_project(project_path, input_file, expected_output_folder)

if __name__ == "__main__":
    main()
