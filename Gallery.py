import os

# Folder Path
Gallery_Folder = "static/photos/"

class Gallery:

    def __init__(self):
        pass

    def get_all_gallery(self):
        galleries = [name for name in os.listdir(Gallery_Folder)]
        return galleries

    def add_gallery(self,gallery_name):
        if os.path.isdir(Gallery_Folder+gallery_name) is False:
            if os.mkdir(Gallery_Folder+gallery_name):
                return True
        else:
            return False

    def delete_gallery(self, gallery_name):
        if os.path.isdir(Gallery_Folder+gallery_name) is True:
            if os.removedirs(Gallery_Folder+gallery_name):
                return True
        return False

    def edit_gallery_name(self,oldName,newName):
        if os.path.isdir(Gallery_Folder+oldName) is True:
            if os.rename(Gallery_Folder+oldName, Gallery_Folder+newName):
                return True
        else:
            return False

class Photos:

    def __init__(self):
        pass

    def get_all_gallery_photos(self, gallery_name):
        photos=[]
        for name in os.listdir(Gallery_Folder+gallery_name):
            if(name.split(".")[0] != "Thumbs"):
                photos.append(name)
        return photos

    def delete_gallery_photos(self, gallery_name, photo_name):
        # Check For the existense of photo or directory
        if os.path.exists(Gallery_Folder + gallery_name+"/"+photo_name) is True:
            if os.remove(Gallery_Folder+gallery_name+"/"+photo_name):
                return True
        return False
