import tkinter as tk

class Application(tk.Frame):
	def __init__(self, master, info, call=None):
		super().__init__(master)
		self.call = call

		master.geometry('800x600')
		self.master = master
		self.pack()
		
		self.MixGames=tk.IntVar()
		self.MixSfx=tk.IntVar()
		self.MixMusic=tk.IntVar()
		self.MixDialogs=tk.IntVar()

		self.MixCharacters=tk.IntVar()
		self.MixEpisodes=tk.IntVar()

		self.MixSfxWithDialogs=tk.IntVar()

		self.Seed = tk.StringVar()

		self.info = info
		self.games = []
		self.copyFromInfo()

		self.createWidgets()

		self.update()



	def createWidgets(self):
		
		self.FSettings = tk.Frame(self)
		self.FSettings.pack(side="top")


		self.FSeed = tk.Frame(self.FSettings)
		self.FSeed.pack(side="top")

		LSeed = tk.Label(self.FSeed, text="Seed")
		LSeed.pack(side="left")

		ESeed = tk.Entry(self.FSeed, textvariable=self.Seed)
		ESeed.pack(side="left")

		# BSeed = tk.Checkbutton(self.FSeed, variable=game["mix"], command=self.update, selectcolor="blue")
		# BSeed.pack(side="left")

		#First column
		self.FSfxDialogOut = tk.Frame(self.FSettings)
		self.FSfxDialogOut.pack(side="left")

		#One row
		self.FSfxDialogIn = tk.Frame(self.FSfxDialogOut)
		self.FSfxDialogIn.pack(side="top")

		self.BMixSfx = tk.Checkbutton(self.FSfxDialogIn, text = "Mix Sfx", variable=self.MixSfx, command=self.update, selectcolor="blue")
		self.BMixSfx.pack(side="left")

		self.BMixDialogs = tk.Checkbutton(self.FSfxDialogIn, text = "Mix Dialogs", variable=self.MixDialogs, command=self.update, selectcolor="blue")
		self.BMixDialogs.pack(side="left")

		#Under them
		self.BMixSfxWithDialogs = tk.Checkbutton(self.FSfxDialogOut, text = "Mix Sfx with Dialogs", variable=self.MixSfxWithDialogs, command=self.update, selectcolor="blue", state="disabled")
		self.BMixSfxWithDialogs.pack(side="top")

		#Other column
		self.BMixMusic = tk.Checkbutton(self.FSettings, text = "Mix Music", variable=self.MixMusic, command=self.update, selectcolor="blue")
		self.BMixMusic.pack(side="left")


		#Mid bottom
		
		self.createGameRows()


		self.Shuffle = tk.Button(self, text="Shuffle", fg="red",
		command=self.execute)
		self.Shuffle.pack(side="bottom")

	def createGame(self, name, Vmix=0, Vdir=""):
		dir = tk.StringVar(value=Vdir)
		mix = tk.IntVar(value=Vmix)

		dic = {
			"dir":dir,
			"name":name,
			"mix":mix
		}
		self.games.append(dic)

	def createGameRows(self):
		for game in self.games:
			Fgame = tk.Frame(self)
			Fgame.pack(side="top")

			Lgame = tk.Label(Fgame, text=game["name"])
			Lgame.pack(side="left")

			Egame = tk.Entry(Fgame, textvariable=game["dir"])
			Egame.pack(side="left")

			Bgame = tk.Checkbutton(Fgame, variable=game["mix"], command=self.update, selectcolor="blue")
			Bgame.pack(side="left")


	def update(self):
		if self.MixSfx.get() == 1 and self.MixDialogs.get() == 1:
			self.BMixSfxWithDialogs["state"] = "normal"
		else:
			self.BMixSfxWithDialogs["state"] = "disabled"
		self.copyToInfo()

	def copyToInfo(self):
		self.info["settings"]["Seed"] = self.Seed.get()
		self.info["settings"]["MixGames"] = self.MixGames.get()
		self.info["settings"]["MixSfx"] = self.MixSfx.get()
		self.info["settings"]["MixMusic"] = self.MixMusic.get()
		self.info["settings"]["MixDialogs"] = self.MixDialogs.get()

		self.info["settings"]["MixCharacters"] = self.MixCharacters.get()
		self.info["settings"]["MixEpisodes"] = self.MixEpisodes.get()

		self.info["settings"]["MixSfxWithDialogs"] = self.MixSfxWithDialogs.get()

		self.info["games"]=[]
		for game in self.games:
			dic = {}
			dic["dir"] = game["dir"].get()
			dic["type"] = game["name"]
			dic["mix"] = game["mix"].get()
			self.info["games"].append(dic)



	def copyFromInfo(self):
		self.Seed.set( self.info["settings"]["Seed"] )
		self.MixGames.set( self.info["settings"]["MixGames"] )
		self.MixSfx.set( self.info["settings"]["MixSfx"] )
		self.MixMusic.set( self.info["settings"]["MixMusic"] )
		self.MixDialogs.set( self.info["settings"]["MixDialogs"] )

		self.MixCharacters.set( self.info["settings"]["MixCharacters"] )
		self.MixEpisodes.set( self.info["settings"]["MixEpisodes"] )

		self.MixSfxWithDialogs.set( self.info["settings"]["MixSfxWithDialogs"] )

		for game in self.info["games"]:
			self.createGame(game["type"],game["mix"],game["dir"])








	def execute(self):
		self.copyToInfo()
		self.master.destroy()
		self.call()
