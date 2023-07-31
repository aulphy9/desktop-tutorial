import os
import zipfile
import pandas as pd

#function to run the code file .py or .java in the terminal
def run_code_file(code_file, input_line):
    # Determine the file type
    file_extension = os.path.splitext(code_file)[1].lower()

    #get the name of the file without the extension 
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
        #set that to current directory
        os.chdir(class_dir)
        # Execute the command and capture the output
        command= f"java {class_name}"
    else:
        print(f"Unsupported file type: {file_extension}")
        return None
    
    #open a temp file and write the line of input to the file (to be used in the command)
    with open("temp.txt", "w") as temp_file:
        temp_file.write(input_line)
    
    #add the input file to the command
    command +=f" < temp.txt"
    #run the command and save the output
    output = os.popen(command).read()

    #remove the temp file created earlier
    os.remove("temp.txt")
    #switch back to original directory
    os.chdir(original_dir)

    #return the output received from running

    return output
def insert_grade(csv_file_path, last_name, first_name, grade):
    try:
        # Read the CSV file 
        df = pd.read_csv(csv_file_path)

        # Find the matching rows based on last name and first name
        mask = (df['Last Name'] == last_name) & (df['First Name'] == first_name)

        # error handling if no match of last name or first name is used
        if not any(mask):
            print(f"No record found for {first_name} {last_name}.")
            return False

        #set the value based on the row found
        df.loc[mask, df.columns[3]] = grade

        # Save to csv
        df.to_csv(csv_file_path, index=False)

        #Output success 
        print(f"Grade inserted successfully for {first_name} {last_name}.")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

#function to compare the output between the expected output file in the folder and the output from run_code_file
def compare_output(output, expected_output_file):
    #open the expected output file
    with open(expected_output_file, 'r') as f:
        #sort through the blank lines in the expected output file
        expected_output = [line for line in f.readlines() if line.strip()]

    #sort through the blank lines in in the output provided
    output_lines = [line for line in output.strip().split('\n') if line.strip()]
    #save the number of lines from each output
    num_expected_lines = len(expected_output)
    num_output_lines = len(output_lines)
    num_correct_lines = 0

    #loop through as many times as the minimum of the two
    for i in range(min(num_expected_lines, num_output_lines)):
        if output_lines[i].strip() == expected_output[i].strip():
            num_correct_lines += 1

    #Divide the number of correct lines provided and the number that was expected from the expected output
    correctness_percentage = (num_correct_lines / num_expected_lines) * 100
    return correctness_percentage

#function to evaluate each student 
def evaluate_project(project_path, input_folder, expected_output_folder, grades_file):
    #split the project path then split by - and split by a space to get the first and last names of students
    split_by_slash=project_path.split("\\")
    folder_name=split_by_slash[1].split("-")
    last_and_first=folder_name[2].split(" ")
    last_name=last_and_first[2]
    first_name=last_and_first[1]
    #code is located in each student's src path
    src_path = os.path.join(project_path, folder_name[-1][1:], "src")
    #print(src_path)
    print(f"Grading {first_name} {last_name}")
    

    num_files=0
    correctness_percentage=0
    #loop through the source folder of each student to access each code file
    for root, _, files in os.walk(src_path):
        for file in files:
            code_file = os.path.join(root, file)
            #replace the extension to .txt for both expected output and input in order to get the correct files
            expected_output_file = os.path.join(expected_output_folder, file.replace('.py', '.txt').replace('.java', '.txt'))
            input_file=os.path.join(input_folder, file.replace('.py', '.txt').replace('.java', '.txt'))

            if os.path.isfile(expected_output_file):
                output=''
                with open(input_file, "r") as f:
                    #loop through input file and run the code by the times of lines in the input file
                    for line in f:
                        temp = run_code_file(code_file, line)
                        #add the output by each input into a total output
                        if temp is not None:
                            output+=temp
                #after the total output is compiled, compare the output with the expected output file
                correctness_percentage += compare_output(output, expected_output_file)
                num_files+=1
                #student score is the amount of points received from correctness divided by num of files
                print(f"{file} Student Score: {(correctness_percentage/num_files):.2f}%")
        #insert the grade into the CSV file
        insert_grade(grades_file, last_name, first_name, correctness_percentage)
        

#function to unzip a folder
def unzip(folder_path):
    #save the newly unzipped folder into the same path 
    zip_directory = folder_path[:-4]

    #make the folder if it does not exist
    if not os.path.exists(zip_directory):
        os.makedirs(zip_directory)

    # extract the contents of the zip
    try:
        with zipfile.ZipFile(folder_path, 'r') as zip_ref:
            #unzip the original folder path into the new folder created
            zip_ref.extractall(zip_directory)

        #print("Unzip successful.")
        #return the path of the newly created unzipped folder
        return folder_path[:-4]
    #error handling for zip files 
    except zipfile.BadZipFile:
        print("Error: Invalid ZIP file.")
        return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

#main function that takes all the input from the GUI
def main_function(project_folder, input_folder, expected_output_folder, grades_file):
    #unzip the big zip folder from D2L
    unzipped_project=unzip(project_folder)

    #delete the index.html from the big folder
    if os.path.exists(os.path.join(unzipped_project, "index.html")):
        os.remove(os.path.join(unzipped_project, "index.html"))
    #loop through every student porject
    for project in os.listdir(unzipped_project):
        project_path = os.path.join(unzipped_project, project)
        #unzip each student project
        unzipped=unzip(project_path)
        if os.path.isdir(unzipped):
            #evaluate each student project
            evaluate_project(unzipped, input_folder, expected_output_folder, grades_file)
    
    print("Grading Complete")

if __name__ == "__main__":
    main_function()

