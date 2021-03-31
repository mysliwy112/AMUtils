import sys
import os
import struct as st

data=[]
with open(sys.argv[1],"br") as arch:
	data=arch.read()
filePos=st.unpack_from("<I", data, offset=8)[0]
fileNum=st.unpack_from("<I", data, offset=filePos)[0]
filePos+=4
for i in range(0,fileNum):
	filenameLen=st.unpack_from("<B", data, offset=filePos)[0]
	filePos+=1
	filename=data[filePos:filePos+filenameLen].decode('Windows-1250')
	filePos+=filenameLen
	fileSiz=st.unpack_from("<I", data, offset=filePos)[0]
	filePos+=4
	fileOff=st.unpack_from("<I", data, offset=filePos)[0]
	filePos+=8
	fileData=data[fileOff:fileOff+fileSiz]
	filename=("dane\\"+filename).replace("\\","/")

	if not os.path.exists(os.path.dirname(filename)):
		os.makedirs(os.path.dirname(filename))
	with open(filename,"wb+") as file:
		file.write(fileData)