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

def open_item(name, type, path):
    file_path = os.path.join(path, name)
    subprocess.run(["open", file_path])
    switch_followup(name, type, path)
    
    
def delete(name, type, path):
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
    new_name = questionary.text("What would you like to rename it to?", default=name).ask()
    if validate_file_folder_name(new_name) == False:
        print("invalid name")
        return
    else:
        try:
            os.rename(os.path.join(path, name), os.path.join(path, new_name))
        except FileExistsError:
            print('File already exists, please try again.')
            rename(name, type, path)
            

def validate_new_location(source_path, destination_path):
    # Check if an item with the same name exists at the destination
    if os.path.exists(destination_path):
        return False
    
    return True

def move_item(source_path, destination_path):
    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)
    
def move(name, type, path):
    ans = questionary.select(
        f"Where would you like to move {name} to?",
        choices=["choose location", "new folder"]
    ).ask()
    if ans == "choose location":
        desitination = questionary.path(
            "Where would you like to move it to?", default=os.getcwd(), only_directories=True, 
        ).ask() 
        move_item(os.path.join(path, name), desitination) if validate_new_location(os.path.join(path, name), os.path.join(desitination, name)) == True else print("invalid location")
    elif ans == "new folder":
        new_folder_name = questionary.text("What would you like to name the new folder?", default='').ask()
        if validate_file_folder_name(new_folder_name) == False:
            print("Folder name invalid, please try again.") 
            move(name, type, path)
            return
        else:
            try:
                os.mkdir(os.path.join(path, new_folder_name))
                move_item(os.path.join(path, name), os.path.join(path, new_folder_name))
            except FileExistsError:
                print("Folder already exists, please try again.")
                move(name, type, path)
                return
    reorg('Cleaner')

def reorg(base_path=None):
    apple_script = """
    
-- Based on  https://gist.github.com/mrienstra/8330528
-- Which is based on http://www.tuaw.com/2012/12/24/applescript-desktop-icon-race/
-- Current known limitations: Does not work with "Label position" set to "Right" (specifically, icons will overlap), desktop width and height are hardcoded according to my specific machine 

-- Adjust these for different spacing
property theSpacingFactor : 1.0
property theGutterXFactor : 0.57
property theGutterYFactor : 0.57



on rearrangeDesktopIcons()
	tell application "Finder"
		tell icon view options of window of desktop
			set theArrangement to arrangement
			set theArrangementString to theArrangement as string
			
			set theIconSize to icon size
			set theLabelSize to text size
		end tell
		
	
		set theDesktopBounds to bounds of window of desktop
		set theDesktopWidth to 1440 
		set theDesktopHeight to 900 



		-- Retrieve a list of items on the desktop
		set theDesktopItems to every item of desktop
		set theContestantOffset to theIconSize / 2
		
		set theSpacing to (theIconSize + theLabelSize + theContestantOffset) * theSpacingFactor
		set theGuttersX to theSpacing * theGutterXFactor
		set theGuttersY to theSpacing * theGutterYFactor
		set theMaxColumns to ((theDesktopWidth - theGuttersX * 2) / theSpacing) as integer 
		set theMaxRows to ((theDesktopHeight - theGuttersY * 2) / theSpacing) as integer
		set theMaxLocations to theMaxRows * theMaxColumns

		set y to 1
		repeat with a from 1 to length of theDesktopItems
	
			set x to a mod theMaxColumns
			if x is 0 then
				set x to theMaxColumns
			end if
			
			if a is greater than theMaxLocations then
				set desktop position of item a of theDesktopItems to {theGuttersX, theGuttersY}
			else
				set desktop position of item a of theDesktopItems to {theGuttersX + (x - 1) * theSpacing + 120, theGuttersY + (y - 1) * theSpacing}

			end if
			
			if a mod theMaxColumns is 0 then
				set y to y + 1
			end if
		end repeat
	end tell
end rearrangeDesktopIcons

on adding folder items to alias after receiving listOfAlias
	rearrangeDesktopIcons()
end adding folder items to

on removing folder items from alias after losing listOfAliasOrText
	rearrangeDesktopIcons()
end removing folder items from

rearrangeDesktopIcons()

   """ 
    with open('tmp_script.applescript', 'w') as script_file:
        script_file.write(apple_script)

# Run the AppleScript using the osascript command
    subprocess.run(["osascript", "tmp_script.applescript"])

# Clean up by deleting the temporary script file
    subprocess.run(["rm", "tmp_script.applescript"])
    # subprocess.run(['osascript', './' + base_path + '/cleanDesktop.applescript'])

def switch(ans, name, type, path):
    if ans == "delete":
        delete(name, type, path)
    elif ans == "rename":
        rename(name, type, path)
    elif ans == "move":
        move(name, type, path)
    elif ans == "open":
        open_item(name, type, path)

        
def switch_followup(name, type, path):
    ans = questionary.select(
        f"Would you like to do anything else with your {type} named {name}?",
        choices=["delete", "rename", "move", "next"]
        ).ask()
    if ans is None:
        return
    else:
        switch(ans, name, type, path)    

def processItems(items, path):
    
    file_folder_info = [{"name": item, "type": "directory" if os.path.isdir(os.path.join(path, item)) else "file"} for item in items]
    
    for item in file_folder_info:
        name, type = item.values()
        ans = questionary.select(
            f"What would you like to do with your {type} named {name}?",
            choices=["delete", "rename", "move", "open", "next"]
            ).ask()
        if ans is None:
            break
        else:
            switch(ans, name, type, path)
            
    
def main():
    clean_or_org = questionary.select(
        "Hey welcome to the cleaner. Would you like to re-organize your desktop or clean and re-organize your desktop?", 
        choices=["re-org", "clean"]
        ).ask()
    
    if(clean_or_org == "re-org"):
        reorg()
    else: 
        os.chdir(os.path.expanduser("~"))
        path = questionary.path(
            "Please enter the path to your Desktop", default=os.getcwd(), only_directories=True, validate=DirectoryValidator()
        ).ask()
        items = os.listdir(path)
        os.chdir(path)
        processItems(items, path)


if __name__ == "__main__":
    main()


# pretty happy with where this application is at...one thing i'd like to see improved though is the ability to move the icons on your desktop into a better layout etc...
# maybe even with differnt types of layouts etc...
