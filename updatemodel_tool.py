# readme 
# python -m PyInstaller --onefile .\updatemodel_tool.py 
# python3 -m PyInstaller --onefile .\updatemodel_tool.py 
# -w: no terminal required 
# Run: updatemodel_tool.exe EMPTY/DYV4

import os
import sys
import shutil
import json
from datetime import datetime, timezone
from sys import platform

DEBUG= False

def debug_print(message):
    if DEBUG:
        print(message)

# declear common file paths
usrmodel_path = os.path.abspath(os.path.dirname(sys.argv[0]))
for file_user_model in os.listdir(usrmodel_path):
    if file_user_model.endswith(".nb"):
        debug_print(os.path.join(usrmodel_path, file_user_model))
        # Get the file name without the file type extension recursively
        file_user_model_no_ext = os.path.splitext(os.path.basename(file_user_model))[0]
        debug_print(file_user_model_no_ext)

if platform == "win32":
    # Windows...
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    ameba_model_path = os.path.join(desktop, 'AmebaModel')
    debug_print(desktop)
    arduino15_path = os.path.expanduser("~\AppData\Local\Arduino15")
    ambpro2_path = arduino15_path + "\packages\\realtek\hardware\AmebaPro2"
    sdk_version = os.listdir(ambpro2_path)[0]
    dest_path = ambpro2_path + "\\" + sdk_version + "\\variants\common_nn_models"
elif platform == "linux" or platform == "linux2":
    # linux
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    ameba_model_path = os.path.join(desktop, 'AmebaModel')
    debug_print(desktop)
    arduino15_path = os.path.expanduser("/home/" + os.getlogin() + "/.arduino15")
    ambpro2_path = arduino15_path + "/packages/realtek/hardware/AmebaPro2/"
    sdk_version = os.listdir(ambpro2_path)[0]
    dest_path = ambpro2_path + "/" + sdk_version + "/variants/common_nn_models"
elif platform == "darwin":
    # OS X
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    ameba_model_path = os.path.join(desktop, 'AmebaModel')
    debug_print(desktop)
    arduino15_path = os.path.expanduser("/Users/" + os.getlogin() + "/Library/Arduino15")
    ambpro2_path = arduino15_path + "/packages/realtek/hardware/AmebaPro2/"
    sdk_version = os.listdir(ambpro2_path)[1]
    dest_path = ambpro2_path + "/" + sdk_version + "/variants/common_nn_models"

allowed_values = [
    "CYV3", "CYV4", "CYV7", "CM8", "CM16", "CS32", "CS64", 
    "DYV3", "DYV4", "DYV7", "DM8", "DM16", "DS32", "DS64",
    "YVNo", "SNo", "MNo"
]

def dspFileProp(filename):
    file_model_stats = os.stat(filename)
    file_model_datetime = datetime.fromtimestamp(file_model_stats.st_mtime, tz = timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    file_model_date = datetime.fromtimestamp(file_model_stats.st_mtime, tz = timezone.utc).strftime('%Y-%m-%d')
    file_model_mode = oct(file_model_stats.st_mode)
    debug_print("              FILE INFO")
    debug_print("------------------------------------------")
    debug_print(f"Size:          {file_model_stats.st_size}")
    debug_print(f"Last modified: {file_model_datetime}")
    debug_print(f"Mode:          {file_model_mode}")
    debug_print("------------------------------------------")
    return file_model_date

def renameFile(filename, type):
    if type == 1:
        # Backup Dmodel
        filename_modified = "Dbackup_" + dspFileProp(filename) + "_" + filename
        if os.path.isfile(os.path.join(dest_path, filename_modified)) == False:
            os.rename(os.path.join(dest_path, filename), os.path.join(dest_path, filename_modified))
        debug_print("[INFO] Dmodel Backup done.")
    else:
        # Backup Cmodel
        filename_modified = "Cbackup_" + dspFileProp(filename) + "_" + filename
        if os.path.isfile(os.path.join(dest_path, filename_modified)) == False:
            os.rename(os.path.join(dest_path, filename), os.path.join(dest_path, filename_modified))
        debug_print("[INFO] Cmodel Backup done.")

def backupModel(user_model):
    debug_print("[INFO] Backup Default Model: " + input2model(user_model))
    for dest_file in os.listdir(dest_path):
        if "Dbackup" in dest_file:
            debug_print(f"[INFO] Backup Default Model {user_model} found !!!")
        elif input2model(user_model) in dest_file:
            # backup default model
            renameFile(input2model(user_model) + ".nb", 1)
    
    # backup Cmodel
    if platform == "linux" or platform == "linux2" or platform == "darwin" : 
            # linux & OS X
        shutil.copy(usrmodel_path + "/" + file_user_model, dest_path)
    #                     # elif platform == "darwin":
    #                     #     # OS X
    elif platform == "win32":
    #                         # Windows...
        shutil.copy(usrmodel_path + "\\" + input2model(user_model) + ".nb", dest_path)
    debug_print(input2model(user_model) + ".nb")
    renameFile(input2model(user_model) + ".nb", 0)

    # copy Cmodel
    if platform == "linux" or platform == "linux2" or platform == "darwin" : 
            # linux & OS X
        shutil.copy(usrmodel_path + "/" + file_user_model, dest_path)
    #                     # elif platform == "darwin":
    #                     #     # OS X
    elif platform == "win32":
    #                         # Windows...
        shutil.copy(usrmodel_path + "\\" + input2model(user_model) + ".nb", dest_path)
    debug_print("[INFO] User model copied.")

def revertModel(user_model):
    for dest_file in os.listdir(dest_path):
        if "Dbackup" in dest_file:
            debug_print(f"[INFO] Defaut backup model {dest_file} found")
            file_model_reverted = dest_file.split("_", 2)[2]
            if os.path.exists(dest_path + "/" + file_model_reverted):
                if platform == "linux" or platform == "linux2" or platform == "darwin" : 
                    # linux & OS X
                    os.remove(dest_path + "/" + file_model_reverted)
                elif platform == "win32":
                    # Windows...
                    os.remove(dest_path + "\\" + file_model_reverted)
                debug_print(f"[INFO] User Model {file_model_reverted} has been removed")
            # revert Dbackup
            os.rename(os.path.join(dest_path, dest_file), os.path.join(dest_path, file_model_reverted))
            debug_print("[INFO] Revert done.")

def updateJSON(input):
    for file_json in os.listdir(dest_path):
        if file_json.endswith(".json"):
            debug_print(file_json)
            debug_print(input2model(input))
            with open(os.path.join(dest_path, file_json), "r+") as file:
                data = json.load(file)
                if input == 'RESET':
                    break
                data["FWFS"]["files"].append(input2model(input))
            with open(os.path.join(dest_path, file_json), "w") as file:
                json.dump(data, file, indent=4)

def dspMenu():
    options = [
        ("CYV3", "Customize Yolov3"),
        ("CYV4", "Customize Yolov4"),
        ("CYV7", "Customize Yolov7"),
        ("CM8",  "Customize MobileFaceNet int8"),
        ("CM16", "Customize MobileFaceNet int16"),
        ("CS32", "Customize SCRFD 576x320"),
        ("CS64", "Customize SCRFD 640x640"),
        ("DYV3", "Default Yolov3"),
        ("DYV4", "Default Yolov4"),
        ("DYV7", "Default Yolov7"),
        ("DM8",  "Customize MobileFaceNet int8"),
        ("DM16", "Customize MobileFaceNet int16"),
        ("DS32", "Customize SCRFD 576x320"),
        ("DS64", "Customize SCRFD 640x640")
    ]
    debug_print("--------------------------")
    debug_print("Input user model:")
    for option in options[:7]:
        debug_print(f"{option[0]}: {option[1]}")
    debug_print("--------------------------")
    debug_print("Input default model:")
    for option in options[7:]:
        debug_print(f"{option[0]}: {option[1]}")
    debug_print("--------------------------")

def input2model(input):
    # convert user parameter into model name
    model_mapping = {
        "CYV3": "yolov3_tiny",
        "CYV4": "yolov4_tiny",
        "CYV7": "yolov7_tiny",
        "CM8": "mobilefacenet_i8",
        "CM16": "mobilefacenet_i16",
        "CS32": "scrfd320p",
        "CS64": "scrfd640",
        "DYV3": "yolov3_tiny",
        "DYV4": "yolov4_tiny",
        "DYV7": "yolov7_tiny",
        "DM8": "mobilefacenet_i8",
        "DM16": "mobilefacenet_i16",
        "DS32": "scrfd320p",
        "DS64": "scrfd640"
    }
    model = model_mapping.get(input)
    return model

def validationCheck(input):
    if input in allowed_values:
        if input[0] == 'C':
            # convert input to model
            input = input2model(input) + ".nb"
            if os.path.isfile(input):
                debug_print(f"[INFO] Customized Model {input} Found!")
                return 1
            else:
                debug_print(f"[Error] Model {input} NOT Found! Please check your input again.")
        if input[0] == 'D':
            debug_print(f"[INFO] Default Model is being selected!")
            return 0
        else:
            raise SystemExit
    else:
        debug_print("[Error] Please enter a valid input.")
        raise SystemExit

if __name__ == '__main__':
    # TODO: customized folder validation
    if not os.path.exists(ameba_model_path):
        print("The AmebaModel folder does not exist on the desktop.")
        raise SystemExit
    else:
        if not os.listdir(ameba_model_path):
            print("The AmebaModel folder is empty.")
            raise SystemExit
        else:
            debug_print("The AmebaModel folder is not empty.")
    
    user_input_flag = False
    while user_input_flag == False:
        dspMenu()
        if len(sys.argv) > 1:
            # User has provided input, so we can access it
            user_input_sub1 = sys.argv[1]
            debug_print(f"User input: {user_input_sub1}")
        else:
            # User has not provided input, so we prompt them to do so
            user_input_sub1 = input("Please provide a valid input > ")
            debug_print(f"User input: {user_input_sub1}")
        user_input_flag = True
        
        if user_input_sub1 == 'RESET':
            # Reset JSON
            for file_json in os.listdir(dest_path):
                if file_json.endswith(".json"):
                    with open(os.path.join(dest_path, file_json), "r+") as file:
                        data = json.load(file)
                        data["FWFS"]["files"] = []
                    with open(os.path.join(dest_path, file_json), "w") as file:
                        json.dump(data, file, indent=4)
        else:
            if validationCheck(user_input_sub1) == 1:
                backupModel(user_input_sub1)
            else:
                revertModel(user_input_sub1)
    
    updateJSON(user_input_sub1) 
    # input("Press Enter to leave the terminal")