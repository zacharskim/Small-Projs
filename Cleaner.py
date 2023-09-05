import questionary
import os
from prompt_toolkit.validation import Validator, ValidationError
import subprocess
import shutil


class DirectoryValidator(Validator):
    def validate(self, document):
        path = document.text
        if not os.path.isdir(path) or len(os.listdir(path)) == 0:
            raise ValidationError(message="This is not a valid directory. It must contain at least one filer/folder and it must be a directory.")

def open(name, type, path):
    file_path = os.path.join(path, name)
    subprocess.run(["open", file_path])
    
    
    
def delete(name, type, path):
    print('oof', name, type, path)
    if type == 'file':
        os.remove(os.path.join(path, name))
    elif type == 'directory':
        shutil.rmtree(os.path.join(path, name)) 
       
def validate_file_folder_name(name):
    # Check for prohibited characters
    if '/' in name:
        return False

    # Ensure name isn't only spaces
    if name.strip() == "":
        return False

    # Check length constraint
    if len(name) > 255:
        return False

    return True
     
        
def rename(name, type, path):
    print('ahh')
    new_name = questionary.text("What would you like to rename it to?", default=name).ask()
    if validate_file_folder_name(new_name) == False:
        print("invalid name")
        return
    else:
        #must validate the rename, also must have a way to recieve the new_name variable / data....
        #should prolly handle renaming folers / files that are duplicates / already exist, same with moving them...
        os.rename(os.path.join(path, name), os.path.join(path, new_name))
    
def validate_new_location(source_path, destination_path):
    # Check if an item with the same name exists at the destination
    if os.path.exists(destination_path):
        return False
    
    return True

def move_item(source_path, destination_path):
    print(source_path, destination_path, 'huh')
    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)
    
def move(name, type, path):
    ans = questionary.select(
        f"Where would you like to move {name} to?",
        choices=["choose location", "new folder", "go back"]
    ).ask()
    if ans == "choose location":
        desitination = questionary.path(
            "Where would you like to move it to?", default=os.getcwd(), only_directories=True, 
        ).ask() 
        move_item(os.path.join(path, name), desitination) if validate_new_location(os.path.join(path, name), os.path.join(desitination, name)) == True else print("invalid location")
    elif ans == "new folder":
        new_folder_name = questionary.text("What would you like to name the new folder?", default=name).ask()
        if validate_file_folder_name(new_folder_name) == False:
            print("invalid name") #figure out how to let 'em try again...
            return
        else: 
            os.mkdir(os.path.join(path, new_folder_name))
            move_item(os.path.join(path, name), os.path.join(path, new_folder_name))
    else:
        return

        #get the new path, validate the new path, complete the move
        #if validation fails on namne, then let the user rename the file / folder and try again
        #if the validation fails on location, let the user create a new folder there if they want...
        #if the validation fails for some other reason, just send out a generic error ig...
        
    #allow the user to move into a new folder if they want, or just move to a new location etc...
    #  if os.path.exists(source_path):
    #     shutil.move(source_path, destination_path)
    # else:
    #     print(f"{source_path} does not exist.")
    
    

def switch(ans, name, type, path):
    if ans == "delete":
        print("delete")
        delete(name, type, path)
    elif ans == "rename":
        print("rename")
        rename(name, type, path)
    elif ans == "move":
        print("move")
        move(name, type, path)
    elif ans == "open":
        print("open")
        #should we keep track of the opened files and ask the user what they'd like to do with them at the end?, prolly....
        open(name, type, path)
    # else:
        # print("skipp")

def processItems(items, path):
    
    file_folder_info = [{"name": item, "type": "directory" if os.path.isdir(os.path.join(path, item)) else "file"} for item in items]
    
    for item in file_folder_info:
        name, type = item.values()
        ans = questionary.select(
            f"What would you like to do with your {type} named {name}?",
            choices=["delete", "rename", "move", "open", "skip"]
        ).ask()
        if ans is None:
            break
        else:
            switch(ans, name, type, path)
            
    
def main():
    clean_or_org = questionary.select(
        "Hey welcome to the cleaner, let’s get this bread. Would you like re-org the file / folder icons on your desktop or clean a specific location?", 
        choices=["re-org", "clean"]
        ).ask()
    
    if(clean_or_org == "re-org"):
        print("re-org")
    else: 
        os.chdir(os.path.expanduser("~"))
        path = questionary.path(
            "Where would you like to clean?", default=os.getcwd(), only_directories=True, validate=DirectoryValidator()
        ).ask()
        items = os.listdir(path)
        os.chdir(path)
        processItems(items, path)

# current state of the proj
# need to figure out the way to organize the actual icons of the files / folders on the desktop
# need to figure out / implement some error handling for the user input and just the flow of the program in general (how is an error handled / thrown?)
# essentailly, flesh out move, rename, validate_file_folder_name, make a function or functions for organizing files/folder icons...
# make program into an executable again too, that was pretty cool
# figure out how to allow users to cd into folders and cd out of them so they can organize further if they'd like...       
        
        
# basically all i want this program to do is to take all the files on a users desktop and help them organize it 
# so if it's already kinda organized they can just skip touching that folder and it's sub files / folders
# or they can go into that folder and move files around / organize it further - this needs to be implemented 
# it should be a serious of questions that ask the user what they want to do
# the user can choose etc...


if __name__ == "__main__":
    main()
