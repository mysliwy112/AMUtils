# MIT License

# Copyright (c) 2021 mysliwy112

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
