import os
import argparse
import shutil
import copy
import random
import gui
import tkinter	as tk
import yaml

info = {
	"games":[
		{
			"dir":r"",
			"type":"RiSP",
			"mix":True
		},
		{
			"dir":r"",
			"type":"RiU",
			"mix":True
		},
		{
			"dir":r"",
			"type":"RiC",
			"mix":True
		},
		{
			"dir":r"",
			"type":"RiWC",
			"mix":True
		},
		{
			"dir":r"",
			"type":"RiKN",
			"mix":True
		},

	],

	"settings":{

		"MixGames":False,
		"MixSfx":True,
		"MixMusic":False,
		"MixDialogs":True,

		"MixCharacters":False,
		"MixEpisodes":True,

		"MixSfxWithDialogs":1,

		"Seed":""
	}

}


def main():

	lists = {
		"music":[],
		"dialogs":[],
		"sfx":[]
	}
	
	for game in info["games"]:
		print("Mixing ",game["dir"])
		path = game["dir"]
		backupPath = os.path.join(path,"backup")




		if not os.path.isdir(backupPath):
			os.mkdir(backupPath)
			backup = True

		for dirName, subdirList, fileList in os.walk(path,topdown=True):
			for s in range( len(subdirList) - 1, -1, -1):
				check = subdirList[s].lower()
				if check != "wavs" and check != "sfx":
					del subdirList[s]
			
			for file in fileList:
				if not os.path.isdir(os.path.join(backupPath,dirName[len(path):])):
					os.mkdir(os.path.join(backupPath,dirName[len(path):]))
				file = os.path.join(dirName[len(path):], file)
				if file[-4:] == ".wav":
					if not os.path.isfile(os.path.join(backupPath,file)):
						os.rename(os.path.join(path,file),os.path.join(backupPath,file))
					segregate(lists, file)

		notMixed = copy.deepcopy(lists)
		mix(lists, info["settings"]["Seed"])
		info["settings"]["seed"] = ""

		for key in lists:
			for fr,to in zip(notMixed[key],lists[key]):
				try:
					print("Copying ",fr," to ",to)
					shutil.copyfile(os.path.join(backupPath,fr),os.path.join(path,to))
				except shutil.SameFileError:
					pass

			


def segregate(lists, file):
	if isMusic(file):
		lists["music"].append(file)
	else:
		if info["settings"]["MixSfxWithDialogs"]:
			lists["dialogs"].append(file)
		else:
			if isSfx(file):
				lists["sfx"].append(file)
			else:
				lists["dialogs"].append(file)
		
def mix(lists, seed):
	random.seed(seed,2)
	if info["settings"]["MixMusic"]:
		random.shuffle(lists["music"])
	if info["settings"]["MixDialogs"]:
		random.shuffle(lists["dialogs"])
	if info["settings"]["MixSfx"]:
		random.shuffle(lists["sfx"])


def isSfx(str):
	return "sfx" in str

def isMusic(str):
	return '/' not in str

def loadInfo():
	global info
	if os.path.isfile("config.yml"):
		with open('config.yml', 'r') as file:
			info2 = yaml.safe_load(file)
			if "settings" in info2:
				for key in info2["settings"]:
					info["settings"][key] = info2["settings"][key]
			if "games" in info2:
					info["games"] = info2["games"]
	else:
		print("Can't find configuration file, loading defaults...")

def saveInfo():
	global info
	with open('config.yml', 'w') as file:
		yaml.dump(info, file)



loadInfo()
if info["settings"]["Seed"] == "":
	info["settings"]["Seed"] = random.randrange(10000000000000)
print(info)

root = tk.Tk()
app = gui.Application(root, info, main)
app.mainloop()
saveInfo()
