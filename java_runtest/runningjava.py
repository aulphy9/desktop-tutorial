import os
import subprocess

output = subprocess.check_output("C:\\CP317\\desktop-tutorial\\java_runtest\\Testing.java", stderr=subprocess.PIPE)
print(output)