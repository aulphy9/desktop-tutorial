import os
import zipfile
import pandas as pd


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
        command = f"javac \"{code_file}\""
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
def insert_grade(csv_file_path, last_name, first_name, grade):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Find the matching rows based on last name and first name
        mask = (df['Last Name'] == last_name) & (df['First Name'] == first_name)

        # If there's no match, return False
        if not any(mask):
            print(f"No record found for {first_name} {last_name}.")
            return False

        df.loc[mask, df.columns[3]] = grade

        # Save the updated DataFrame back to the CSV file
        df.to_csv(csv_file_path, index=False)

        print(f"Grade inserted successfully for {first_name} {last_name}.")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def compare_output(output, expected_output_file):
    with open(expected_output_file, 'r') as f:
        expected_output = [line for line in f.readlines() if line.strip()]

    output_lines = [line for line in output.strip().split('\n') if line.strip()]
    num_expected_lines = len(expected_output)
    num_output_lines = len(output_lines)
    num_correct_lines = 0
    print("in compare output")
    for i in range(min(num_expected_lines, num_output_lines)):
        if output_lines[i].strip() == expected_output[i].strip():
            num_correct_lines += 1

    correctness_percentage = (num_correct_lines / num_expected_lines) * 100
    return correctness_percentage

def evaluate_project(project_path, input_folder, expected_output_folder, grades_file):
    split_by_slash=project_path.split("\\")
    print(split_by_slash)
    folder_name=split_by_slash[1].split("-")
    last_and_first=folder_name[2].split(" ")
    last_name=last_and_first[2]
    first_name=last_and_first[1]
    src_path = os.path.join(project_path, "src")
    print(last_name)
    print(first_name)
    

    num_files=0
    correctness_percentage=0
    for root, _, files in os.walk(src_path):
        for file in files:
            code_file = os.path.join(root, file)
            expected_output_file = os.path.join(expected_output_folder, file.replace('.py', '.txt').replace('.java', '.txt'))
            input_file=os.path.join(input_folder, file.replace('.py', '.txt').replace('.java', '.txt'))

            if os.path.isfile(expected_output_file):
                output=''
                with open(input_file, "r") as f:
                    for line in f:
                        temp = run_code_file(code_file, line)
                        if temp is not None:
                            output+=temp
                correctness_percentage += compare_output(output, expected_output_file)
                num_files+=1
        insert_grade(grades_file, last_name, first_name, correctness_percentage)
        print(f"{file} - Student Score: {(correctness_percentage/num_files):.2f}%")

def unzip(folder_path):
    zip_directory = os.path.dirname(folder_path)

    # Extract the contents of the ZIP file
    try:
        with zipfile.ZipFile(folder_path, 'r') as zip_ref:
            zip_ref.extractall(zip_directory)

        print("Unzip successful.")
        return folder_path[:-4]

    except zipfile.BadZipFile:
        print("Error: Invalid ZIP file.")
        return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def main_function(project_folder, input_folder, expected_output_folder, grades_file):
    #project_folder = "autograder\\test_code_files.zip"
    #input_folder = "autograder\\test_input_files"
    #expected_output_folder = "autograder\\test_output_files"
    #grades_file="autograder\\CP-317-C Shell For SW Testing_GradesExport_2023-07-26-19-17.csv"

    unzipped_project=unzip(project_folder)
    print(unzipped_project)

    for project in os.listdir(unzipped_project):
        project_path = os.path.join(unzipped_project, project)
        unzipped=unzip(project_path)
        print(unzipped)
        if os.path.isdir(unzipped):
            evaluate_project(unzipped, input_folder, expected_output_folder, grades_file)

if __name__ == "__main__":
    main_function()

