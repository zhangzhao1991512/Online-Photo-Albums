import os
import hashlib
path = 'new_images/'
filenames = os.listdir(path)

for i in filenames:
	olddir = os.path.join(path, i) #origin file path
	filename = os.path.splitext(i)[0]
	filetype = os.path.splitext(i)[1]
	if os.path.isdir(olddir):
		continue
	if i[0] == 'f':
		albumid = 2
	elif i[0] == 'w':
		albumid = 3
	elif i[2] == 'a':
		albumid = 4
	else:
		albumid = 1
	m = hashlib.md5((str(albumid)+i).encode('utf-8'))
	m = m.hexdigest()
	newdir = os.path.join(path, m + filetype) #file path to be changed
 	os.rename(olddir, newdir)
 	

