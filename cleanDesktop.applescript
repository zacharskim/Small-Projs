-- https://gist.github.com/mrienstra/8330528
-- Based on http://www.tuaw.com/2012/12/24/applescript-desktop-icon-race/
-- Inspired by http://namesakecomic.com/comic/happy-new-year-from-namesake/#comment-1182035013

-- Rearranges Desktop icons to flow from left to right, top to bottom.

-- To have this run automatically every time files are added or removed from the Desktop, set this script to run as a Desktop "Folder Action". (See https://developer.apple.com/library/mac/documentation/applescript/conceptual/applescriptlangguide/reference/ASLR_folder_actions.html )

-- This is currently a rough proof-of-concept. It has only been tested with OS X 10.8.5 (Mountain Lion).

-- Current known limitations: Does not work with "Label position" set to "Right" (specifically, icons will overlap).



-- Adjust these for different spacing
property theSpacingFactor : 1.0
property theGutterXFactor : 0.57
property theGutterYFactor : 0.57



on rearrangeDesktopIcons()
	tell application "Finder"
		tell icon view options of window of desktop
			set theArrangement to arrangement
			set theArrangementString to theArrangement as string
			if {"not arranged", "«constant ****narr»", "snap to grid", "«constant ****grda»"} does not contain theArrangementString then
				display alert "\"Rearrange Desktop Icons\" AppleScript says:" message "Cannot rearrange Desktop items, please change Desktop \"Sort by\" to \"None\" or \"Snap to Grid\"." giving up after 10
				return
			end if
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


-- change the gutter location, modify the code / repeat loop to fill files from right to left, top to bottom etc...
-- add some light error validation
-- push the code and call it a day...

