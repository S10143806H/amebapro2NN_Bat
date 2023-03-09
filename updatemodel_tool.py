# readme 
# python -m PyInstaller --onefile .\updatemodel_tool.py 
# python3 -m PyInstaller --onefile .\updatemodel_tool.py 
# -w: no terminal required 
# Run: updatemodel_tool.exe 2 DYV4 
#      updatemodel_tool.exe 1 CYV4

import os
import sys
import shutil
import json
import re
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
        # debug_print(os.path.join(usrmodel_path, file_user_model))
        # Get the file name without the file type extension recursively
        file_user_model_no_ext = os.path.splitext(os.path.basename(file_user_model))[0]
        #  debug_print(file_user_model_no_ext)

if platform == "linux" or platform == "linux2":
    # linux
    arduino15_path = os.path.expanduser("/home/" + os.getlogin() + "/.arduino15")
    ambpro2_path = arduino15_path + "/packages/realtek/hardware/AmebaPro2/"
    sdk_version = os.listdir(ambpro2_path)[0]
    dest_path = ambpro2_path + "/" + sdk_version + "/variants/common_nn_models"
elif platform == "darwin":
    # OS X
    arduino15_path = os.path.expanduser("/Users/" + os.getlogin() + "/Library/Arduino15")
    ambpro2_path = arduino15_path + "/packages/realtek/hardware/AmebaPro2/"
    sdk_version = os.listdir(ambpro2_path)[1]
    dest_path = ambpro2_path + "/" + sdk_version + "/variants/common_nn_models"
elif platform == "win32":
    # Windows...
    arduino15_path = os.path.expanduser("~\AppData\Local\Arduino15")
    ambpro2_path = arduino15_path + "\packages\\realtek\hardware\AmebaPro2"
    sdk_version = os.listdir(ambpro2_path)[0]
    dest_path = ambpro2_path + "\\" + sdk_version + "\\variants\common_nn_models"
#debug_print(sdk_version)
#debug_print(dest_path)

# allowed keys
allowed_values = ["CYV3", "CYV4", "CYV7", "CM", "CS", "DYV3", "DYV4", "DYV7", "DM", "DS"]
allowed_Dvalues = []

def backupModel(user_model):
    """
    Check user model whether exists.

    Returns:
    None
    """
    if user_model == "CYV3" or user_model == "DYV3":
        file_user_model_no_ext = "yolov3_tiny"
    elif user_model == "CYV4" or user_model == "DYV4":
        file_user_model_no_ext = "yolov4_tiny"
    elif user_model == "CYV7"or user_model == "DYV7":
        file_user_model_no_ext = "yolov7_tiny"
    elif user_model == "CM" or user_model == "DM" :
        file_user_model_no_ext = "mobilefacenet_i8"
    elif user_model == "CS" or user_model == "DS":
        file_user_model_no_ext = "scrfd320p"
    debug_print(file_user_model_no_ext)
    
    for file_model in os.listdir(dest_path):
        if file_model.endswith(".nb"):
            # debug_print(file_model)
            
            if "backup" in file_model and file_user_model_no_ext in file_model:
                debug_print(f"Error: Backuped Model {file_model} has found !!!")
                # Revert backup model
                file_model_reverted = file_model.split("_", 2)[2]
                debug_print(file_model_reverted)
                # TODO delete copied user file
                os.remove(dest_path + "\\" + file_model_reverted)
                debug_print("INFO: User model deleted.")
                # TODO rename backuped model back to normal
                os.rename(os.path.join(dest_path, file_model), os.path.join(dest_path, file_model_reverted))
                debug_print("INFO: Revert done.")
                break
            else:
                if file_user_model_no_ext in file_model:
                    # TODO file size !=0
                    file_user_model = file_model
                    debug_print(f"Model {file_model} contains the keyword {file_user_model} has found !!!")
                    # Get file properties
                    if os.path.exists(file_user_model_no_ext + ".nb"):
                        file_model_stats = os.stat(file_user_model_no_ext + ".nb")
                        file_model_datetime = datetime.fromtimestamp(file_model_stats.st_mtime, tz = timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                        file_model_mode = oct(file_model_stats.st_mode)
                        debug_print("--------------------------")
                        debug_print("Size:          {file_model_stats.st_size}")
                        debug_print("Last modified: {file_model_datetime}")
                        debug_print("Mode:          {file_model_mode}")
                        debug_print("--------------------------")
                        debug_print("INFO: Backup starts....")
                        # Backup model
                        file_model_modified = "backup_" + datetime.fromtimestamp(file_model_stats.st_mtime, tz = timezone.utc).strftime('%Y-%m-%d') + "_" + file_model
                        os.rename(os.path.join(dest_path, file_model), os.path.join(dest_path, file_model_modified))
                        debug_print("INFO: Backup done.")
                        shutil.copy(usrmodel_path + "\\" + file_user_model, dest_path)
                        debug_print("INFO: User model copied.")
                    else:
                        debug_print(f"The file {file_user_model_no_ext}.nb does not exist.")
                else:  
                    continue
    debug_print("==================================")

def updateJSON(option, user_model):
    """
    Updates a JSON file based on the input parameters.

    Args:
    option (int): 0 for default settings, 1 for user settings.
    user_model (str, optional): The user model to use (required if option is 1).

    Returns:
    None
    """
    debug_print(user_model)
    for file_json in os.listdir(dest_path):
        if file_json.endswith(".json"):
            # debug_print(os.path.join(dest_path, file_json))
            # debug_print(file_json)
            # Read the existing data from the file
            with open(os.path.join(dest_path, file_json), "r+") as file:
                data = json.load(file)
            
            if "YV3" in user_model[1:]:
                debug_print("yolov3_tiny")
            
            if user_model == "CYV3" or user_model == "DYV3":
                file_user_model_no_ext = "yolov3_tiny"
            elif user_model == "CYV4" or user_model == "DYV4":
                file_user_model_no_ext = "yolov4_tiny"
            elif user_model == "CYV7"or user_model == "DYV7":
                file_user_model_no_ext = "yolov7_tiny"
            elif user_model == "CM" or user_model == "DM" :
                file_user_model_no_ext = "mobilefacenet_i8"
            elif user_model == "CS" or user_model == "DS":
                file_user_model_no_ext = "scrfd320p"
            # debug_print(file_user_model_no_ext)
            
            if option == 0:
                # Default Settings
                data["FWFS"]["files"] = ['yolov4_tiny', 'scrfd320p', 'mobilefacenet_i8'] 
            elif option == 1:
                # Update the "files" list in the "FWFS" dictionary based on user model name
                if file_user_model:
                    data["FWFS"]["files"] = [file_user_model_no_ext]
                else:
                    debug_print('Error: user_model parameter is required when option is 1')
                    return
            else:
                debug_print('Error: Invalid option')
                return
            
            # Write the updated data back to the file
            with open(os.path.join(dest_path, file_json), "w") as file:
                json.dump(data, file, indent=4)
            if option == 0:
                debug_print('INFO: JSON file reverted to default successfully.')
            else:
                debug_print('INFO: JSON file updated successfully.')


def get_user_input():
    """
    Displays a menu and prompts the user to select an option.

    Options:
    1. Input user model
    2. Use default settings

    If the user selects option 1, the function prompts the user to enter a user model.
    If the user selects option 2, the function uses default settings.
    """
    user_input_flag = 0
    while user_input_flag == 0:
        debug_print("--------------------------")
        debug_print("Please select an option:")
        debug_print("1. Input user model")
        debug_print("2. Use default settings")
        debug_print("--------------------------")

        if len(sys.argv) > 1:
            # User has provided input, so we can access it
            user_input = sys.argv[1]
            debug_print(f"User input: {user_input}")
        else:
            # User has not provided input, so we prompt them to do so
            debug_print("Error: Please provide input.")
            user_input = input("> ")
            debug_print(f"User input: {user_input}")
        
        if user_input == "1" and user_input_flag == 0:
            while True:
                # Use user model
                debug_print("--------------------------")
                debug_print("Input user model:")
                debug_print("CYV3: Customize Yolov3")
                debug_print("CYV4: Customize Yolov4")
                debug_print("CYV7: Customize Yolov7")
                debug_print("CM: Customize MobileFaceNet")
                debug_print("CS: Customize SCRFD")
                debug_print("--------------------------")
                debug_print("Enter your option: ")
                if len(sys.argv) > 1:
                    # User has provided input, so we can access it
                    user_input_sub1 = sys.argv[2]
                    debug_print(f"User input: {user_input_sub1}")
                else:
                    # User has not provided input, so we prompt them to do so
                    user_input_sub1 = input("> ")
                    debug_print(f"User input: {user_input_sub1}")
                user_input_flag = True
                if user_input_sub1 in allowed_Cvalues:
                    backupModel(user_input_sub1)
                    updateJSON(1, user_input_sub1) 
                    break
                else:
                    debug_print("Invalid choice. Please enter valid user model.")
                    break
                
        elif user_input == "2" and user_input_flag == 0:
            while True:
                # Use default settings
                debug_print("--------------------------")
                debug_print("Input default model:")
                debug_print("DYV3: Default Yolov3")
                debug_print("DYV4: Default Yolov4")
                debug_print("DYV7: Default Yolov7")
                debug_print("DM: Default MobileFaceNet")
                debug_print("DS: Default SCRFD")
                debug_print("--------------------------")
                debug_print("Enter your option: ")
                if len(sys.argv) > 1:
                    # User has provided input, so we can access it
                    user_input_sub1 = sys.argv[2]
                    debug_print(f"User input: {user_input_sub1}")
                else:
                    # User has not provided input, so we prompt them to do so
                    user_input_sub1 = input("> ")
                    debug_print(f"User input: {user_input_sub1}")
                user_input_flag = True
                if user_input_sub1 in allowed_Dvalues:
                    updateJSON(1, user_input_sub1) 
                    break
                else:
                    debug_print("Invalid choice. Please enter valid user model.")
                    break
        else:
            debug_print("Invalid choice. Please enter 1 or 2.")
            break


def get_user_input2():
    """
    Displays a menu and prompts the user to select an option.
    """
    user_input_flag = 0
    while user_input_flag == 0:
        debug_print("--------------------------")
        debug_print("Input user model:")
        debug_print("CYV3: Customize Yolov3")
        debug_print("CYV4: Customize Yolov4")
        debug_print("CYV7: Customize Yolov7")
        debug_print("CM: Customize MobileFaceNet")
        debug_print("CS: Customize SCRFD")
        debug_print("--------------------------")
        debug_print("Input default model:")
        debug_print("DYV3: Default Yolov3")
        debug_print("DYV4: Default Yolov4")
        debug_print("DYV7: Default Yolov7")
        debug_print("DM: Default MobileFaceNet")
        debug_print("DS: Default SCRFD")
        debug_print("--------------------------")
        debug_print("Enter your option: ")
        if len(sys.argv) > 1:
            # User has provided input, so we can access it
            user_input_sub1 = sys.argv[1]
            debug_print(f"User input: {user_input_sub1}")
            user_input_flag = True
            if user_input_sub1 in allowed_values:
                backupModel(user_input_sub1)
                updateJSON(1, user_input_sub1) 
            else:
                debug_print("Invalid choice. Please enter valid user model.")
            break
        else:
            # User has not provided input, so we prompt them to do so
            user_input_sub1 = input("> ")
            debug_print(f"User input: {user_input_sub1}")
            user_input_flag = True
            if user_input_sub1 in allowed_values:
                backupModel(user_input_sub1)
                updateJSON(1, user_input_sub1) 
                break
            else:
                debug_print("Invalid choice. Please enter valid user model.")
                break

#####################################################################################
# Main Function
# Default script location: tools/
#####################################################################################
if __name__ == '__main__':
    get_user_input2()                            # display menu
    # input("Press Enter to leave the terminal")

#################################################################
# TODO: support 3 OS [DONE]
# TODO: multi model support []
# TODO: model size check []
# TODO: arduino.ino YOLOMODEL []
