#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
# Renames recursively jpg-files by the exif-tag "DateTimeOriginal"
#
# Example:
# myImage.jpg -> 20220101_125208_IMG.jpg
#
# Works on: Linux
# depends on: exifread


import os, sys, getopt

    
def getFileExtension(fileName):
    fileNameBase, extension = os.path.splitext(fileName)
    extension = extension.lower()
    return extension
    
def getTags(imageFile):
    import exifread
    image = open( imageFile, 'rb')
    tags = exifread.process_file( image, details=False, stop_tag='EXIF DateTimeOriginal')
    image.close()
    print ("tags:",tags)
    return tags
   
def getDateTimeTag(imageFile):
    tags=getTags(imageFile)
    if 'EXIF DateTimeOriginal' in tags.keys() :
        dateTimeTag=str( tags['EXIF DateTimeOriginal'] )
    else: 
        dateTimeTag=""
    return dateTimeTag
    
def formatDateTime(dateTime):
    return dateTime.replace(":","").replace(" ","_")
        
def newFilename( root, formattedDateTime, suffix, fileExtension ):
    return root + "/" + formattedDateTime + suffix + fileExtension

def showHelp():
    print ('Possible arguments:')
    print ('-p <yourpath>')
    print ('--path <yourpath>')
    print ('No arguments is equal to the argument --path "."')
    return
    
def checkArgs(argv):
    path = "." # Default path is current folder
    # If no arguments have been passed, return "." as crurrent directory
    if len(sys.argv) == 1:
        return path
    else:        
        try:
            opts, args = getopt.getopt(argv[1:],"hp:",["help","path="])
        except getopt.GetoptError:
            showHelp()
            sys.exit("Invalid arguments")
        for opt, arg in opts:
            if opt in ('-h',"--help"):
                showHelp()
                sys.exit(0)
            elif opt in ("-p", "--path"):
                path = arg
            else :
                showHelp()
                sys.exit(0)                
        return path

def main(argv):
    path=checkArgs(argv)  
    # Recursivly find all files in the path
    for root, dirs, files in os.walk( path, topdown=True, onerror=None, followlinks=False):
        for fileName in files:        
            # get file-extension
            fileExtension = getFileExtension(fileName)       
            # Check if the file is a jpg file
            if fileExtension == ".jpg":
                # Get file-path 
                investigatedFile = os.path.join( root, fileName)
                # read file binary and extract tags
                dateTimeTag=getDateTimeTag(investigatedFile)
                # continoue with the next file if the tag was not present
                if dateTimeTag == "":
                    print ( "%s has no EXIF dateTimeOriginal tag. Skipping renaming." % investigatedFile)
                    continue
                # Format date
                formattedDateTime = formatDateTime(dateTimeTag)                
                # Create name for renamed file
                renamedFile = newFilename( root, formattedDateTime, "_IMG", fileExtension)
                # Remember last accessed time and modified time. 
                stat = os.stat(investigatedFile)
                # rename file
                #   os.rename(investigatedFile, renamedFile)
                # Restore original creation time
                #   os.utime(renamedFile, (stat.st_atime, stat.st_mtime))
                print ("Renamed:%s to %s" % (investigatedFile, renamedFile))
            else:
                print ( "%s is not .jpg file." % investigatedFile)

if __name__ == "__main__":
    main(sys.argv)
