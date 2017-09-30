import os
import hashlib
filenames = os.listdir('images/')

pic_file = open("contain_insert.txt", "w")
sequence = 0
for i in filenames:
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
	format_str = """INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES ({sequence}, {album}, "{id}", ""); \n"""
 	sql_command = format_str.format(sequence = sequence, album = albumid, id = m)
 	pic_file.write(sql_command)
 	sequence += 1

pic_file.close()