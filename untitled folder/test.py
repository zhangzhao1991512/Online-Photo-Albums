import os
path = 'a'
filenames = os.listdir(path)
for i in filenames:
	olddir = os.path.join(path, i)
	filename = os.path.splitext(i)[0]
	filetype = os.path.splitext(i)[1]
	newdir = os.path.join(path, "hhh" + filetype)
	os.rename(olddir,newdir)

