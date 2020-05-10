from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import askquestion
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import font
from pathlib import Path
import webbrowser
import sys, os
import re

class File:
	def __init__(self, name, path, c):
		self.name = name
		self.path = path
		self.c = c
	def __getitem__(self,key):
		return getattr(self,key)
	def __setitem__(self, key, value):
		self.__dict__[key] = value

global enc

sbSize	= 50
txSizeD	= 10
txSizeS	= 12
txSizeB = 8
wWidth	= 400
wHeight	= 300
pad		= 5
cBG		= '#000'
cFG		= '#fff'
cDark	= '#222'
cHover	= '#444'
cLK		= '#44a'
zoom	= 2
min		= 5
max		= 41
fnt		= "Segoe UI Light"
fntSys	= "Segoe UI"
theme	= "Light"
attach	= 0
change	= 0
opened	= File(name="",path="",c="")
appname	= "Proton Lite"
rlimit	= 4
enc		= "utf-8"
version	= "v1.0_release"
icon	= os.path.realpath(__file__).replace("app.py","")+'/resources/icon.ico'

dir = os.path.realpath(__file__).replace("app.py","")+"data"
ext = '.pdat'
if not (Path(dir).is_dir()):
	Path(dir).mkdir()
	files = [
		("themes","Light\ncBG=#fff\ncFG=#000\ncDark=#ddd\ncHover=#bbb\ncLK=#44a\nDark\ncBG=#000\ncFG=#fff\ncDark=#222\ncHover=#444\ncLK=#6cf"),
		("user",""),
		("recent","")
	]
	for i in range(0, len(files)):
		f = open(dir+"/"+files[i][0]+ext, "w") 
		f.write(files[i][1])
		f.close()

def zoomIn(x = None):
	global zoom, max
	if (fntTx["size"] < max):
		fntTx.config(size=fntTx["size"]+zoom)

def zoomOut(x = None):
	global zoom, min
	if (fntTx["size"] > min):
		fntTx.config(size=fntTx["size"]-zoom)

def zoomNorm(x = None):
	fntTx.config(size=txSizeD)

def applyFont(f,s):
	global txSizeD, fnt
	fnt = f
	txSizeD = s
	fntTx.config(family=f,size=s)

def confirmSave():
	if (change == 1):
		if askquestion("Save changes", "Your file hasn't been saved! Are you sure you want to continue?", icon='warning') == 'no':
			return True
		else:
			return False
	else:
		return False

def editFont():
	w = Toplevel()
	w.iconbitmap(icon)
	w.title("Select Font")
	w.geometry("400x400")
	
	f = list(font.families())
	f.sort(key = lambda x: x[0])
	
	fr = Frame(w, style='s.Label')
	
	fs = font.Font(family=fnt, size=txSizeD)
	
	l = Label(fr, text="Preview Text 123", style='s.Label', font=fs)
	
	df = 0
	s = Listbox(fr, selectmode=SINGLE, bg=cBG, fg=cFG, highlightthickness=0, highlightcolor=cBG, font=fntSys)
	for i in range(0, len(f)):
		s.insert(i, f[i])
		if (f[i] == fnt):
			df = i
	s.bind('<Double-1>', lambda x: fs.config(family=s.selection_get()))
	s.select_set(df)
	
	t = Scale(fr, from_=min, to=max, orient=HORIZONTAL, style='s.Horizontal.TScale', command=lambda x: fs.config(size=int(t.get())), length=200)
	t.set(txSizeD)
	
	i = Label(fr, text="Current font: "+fnt+", "+str(txSizeD), style='s.Label')
	
	o = Frame(fr, style='s.Label')
	
	b = Button(o, text="Apply", style='s.TButton', command=lambda:[applyFont(s.selection_get(),int(t.get())),i.config(text="Current font: "+s.selection_get()+", "+str(int(t.get())))])
	c = Button(o, text="Cancel", style='s.TButton', command=lambda:[w.destroy()])
	
	s.pack(fill='x', padx=pad, pady=pad)
	t.pack(fill='none')
	i.pack(fill='x', padx=pad, pady=pad)
	l.pack(fill='x', padx=pad, pady=pad)
	o.pack(fill='x', padx=pad, pady=pad)
	b.pack(padx=pad, side="left", pady=0)
	c.pack(padx=pad, side="left", pady=0)
	
	fr.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

def contextmenu(event):
	menu.post(root.winfo_x() + event.x, root.winfo_y() + event.y)

def addRecent(f):
	rr = open(dir+"/recent"+ext, "r")
	c = rr.read().splitlines()
	rr.close()
	co = ""
	if (type(c) is list):
		for i in range(len(c)):
			if (i > len(c)-rlimit):
				co += c[i] + "\n"
	r = open(dir+"/recent"+ext, "w")
	r.write(co+f+"\n")
	r.close()
	if len(c) > rlimit-1:
		rmenu.delete(0)
	rmenu.add_command(label=f, command=openFile(f))

def newFile():
	if confirmSave(): return
	app.e.delete("1.0",END)
	app.master.title(appname)
	change = 0
	opened["name"] = ""
	opened["path"] = ""
	opened["c"] = app.e.get("1.0",END)

def openFile(p = ""):
	if confirmSave(): return
	global opened
	if (p == ""):
		f = askopenfilename()
		if f == '': return
		addRecent(f)
	else:
		f = p
	print(enc)
	try:
		fr = open(f, "r", encoding=enc)
		app.e.delete("1.0",END)
		app.e.insert("1.0",fr.read())
		fr.close()
		opened["name"] = f.split("/")[-1]
		opened["path"] = f
		app.master.title(opened["name"])
		opened["c"] = app.e.get("1.0",END)
	except UnicodeDecodeError:
		showinfo("Error","Selected encoding and file encoding do not match.")

def saveFile(saveas = False):
	global change
	if (opened["path"] == "" or saveas == True):
		f = asksaveasfilename(defaultextension=".txt",filetypes=(("Text files","*.txt"),("All files","*.*")))
		if f == '': return
		fr = open(f, "w", encoding=enc)
		fr.write(app.e.get("1.0", END))
		fr.close()
		opened["path"] = f
		opened["name"] = f.split("/")[-1]
		addRecent(f)
	else:
		fr = open(opened["path"], "w")
		fr.write(app.e.get("1.0", END))
		fr.close()
	change = 0
	if (app.master.title().endswith("*")):
		app.master.title(app.master.title()[:-1])
	opened["c"] = app.e.get("1.0", END)

def switchTheme(to):
	try:
		app
	except:
		return
	global cBG, cFG, cDark, cHover, theme
	
	f = open(dir+"/themes"+ext, "r") 
	t = f.read().splitlines()
	f.close()
	
	c = 0
	co = [None] * 5
	for i in range(0,len(t)):
		if c > 0 and c < 6:
			co[c-1] = (t[i].split("="))[1]
			c += 1
		if (t[i] == to):
			c = 1
	if (co[0] == None):
		co = ['#fff','#000','#ddd','#bbb','#44a']
	
	cBG=co[0]
	cFG=co[1]
	cDark=co[2]
	cHover=co[3]
	cLK=co[4]
	
	app.e.config(selectbackground=cDark, insertbackground=cFG, bg=cBG, fg=cFG)
	app.styTx.configure('s.Label', foreground=cFG, background=cBG, font=fntSys)
	app.styLk.configure('sl.Label', foreground=cLK, background=cBG, font=fntSysU)
	app.styBt.configure('s.TButton',foreground=cFG,background=cDark,font=(fntSys,txSizeB),relief="flat")
	app.styBt.map('s.TButton', background=[('pressed','!disabled',cHover),('active',cHover)], font=[('active',(fntSys,txSizeB))], highlightcolor=[('active','#f00')])
	app.stySc.configure('s.Horizontal.TScale',db=0,foreground='#f00',background=cFG,font=(fntSys,txSizeB),relief="flat")
	
	theme = to

def openHelp():
	w = Toplevel()
	w.iconbitmap(icon)
	w.title("Help")
	w.geometry("{}x{}".format(22*txSizeS,23*txSizeS))
	
	f = Frame(w, style='s.Label')
	l = Label(f, text="Shortcuts:"
	"\n\nIncrease text size: Ctrl + +"
	"\nDecrease text size: Ctrl + -"
	"\nNew file: Ctrl + N"
	"\nSave file: Ctrl + S"
	"\nSave file as: Ctrl + Shift + S"
	"\nOpen file: Ctrl + O"
	"\nView file info:Ctrl + I"
	"\nEdit font: Ctrl + F"
	"\nOpen help: Ctrl + H"
	"\nToggle fullscreen: F11",
	style='s.Label')
	
	l.pack(fill='x', padx=pad, pady=pad)
	f.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)


def web(url):
	webbrowser.open_new(url)

def openAbout():
	w = Toplevel()
	w.iconbitmap(icon)
	w.title("About")
	w.geometry("{}x{}".format(20*txSizeS,11*txSizeS))
	
	f = Frame(w, style='s.Label')
	l = Label(f, text="Version: "+version+"\n\nDeveloped by HJfod", style='s.Label')
	
	g = Label(f, text="Github page", style='sl.Label', cursor="hand2")
	g.bind("<Button-1>", lambda e: web("https://github.com/HJfod/proton-lite"))
	
	l.pack(fill='x', padx=pad, pady=pad)
	g.pack(fill='x', padx=pad, pady=pad)
	f.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

def fileInfo():
	w = Toplevel()
	w.iconbitmap(icon)
	w.title("File information")
	w.geometry("{}x{}".format(20*txSizeS,10*txSizeS))
	
	words = str(len(re.sub(' +', ' ', app.e.get("1.0", END).replace("\n"," ")).split(" "))-1)
	chars = str(len(app.e.get("1.0", END))-1)
	schar = str(len(re.sub(' +', '', app.e.get("1.0", END).replace("\n"," "))))
	
	f = Frame(w, style='s.Label')
	l = Label(f, text="Words: "+words+"\nCharacters: "+chars+"\nWithout spaces: "+schar+"\nPath: "+opened["path"], style='s.Label')
	
	l.pack(fill='x', padx=pad, pady=pad)
	f.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

def tachMenu():
	if (root["menu"] == ''):
		root.config(menu=menu)
	else:
		root.config(menu='')

def on_closing():
	if confirmSave(): return
	
	cont = "theme='"+theme+"'\nattach="+("0"if root["menu"]=='' else"1")+"\nfntTx.config(family='"+fntTx["family"]+"',size="+str(fntTx["size"])+")\nwWidth="+str(wWidth)+"\nwHeight="+str(wHeight)
	
	f = open(dir+"/user"+ext, "w")
	f.write(cont)
	f.close()
	
	root.destroy()

def docChange():
	c = app.e.get("1.0",END)
	if c == "\n": return
	if (c != opened["c"]):
		global change
		change = 1
		if not app.master.title().endswith("*"):
			app.master.title(app.master.title()+"*")

def handleKey(e):
	if e.keycode == 122:
		root.state('zoomed') if root.state() == "normal" else root.state("normal")

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()
		
		self.styTx = Style()
		self.styBt = Style()
		self.styBt.theme_use('clam')
		self.stySc = Style()
		self.styLk = Style()
	
	def init_window(self):
		self.master.title(appname)
		
		self.pack(fill=BOTH, expand=1)
		
		self.e = Text(self, font=fntTx, bg=cBG, fg=cFG, tabs=5, wrap=WORD, selectbackground=cDark, insertbackground=cFG, bd=0, padx=pad, pady=pad, borderwidth=0)
		self.e.place(x=0, y=0, width=wWidth, height=wHeight)
		self.e.bind("<Key>", lambda e:[docChange()])
		
		self.bind('<Configure>', self.resize)

	def resize(self, event):
		global wWidth, wHeight
		w,h = event.width, event.height
		self.e.place(width=w, height=h)
		wWidth = w
		wHeight = h

root = Tk()

fntTx = font.Font(family=fnt, size=txSizeD)
fntSys = font.Font(family=fntSys, size=txSizeS)
fntSysU = font.Font(family=fntSys, size=txSizeS, underline=1)

menu = Menu(root, tearoff=0)

fmenu = Menu(menu, tearoff=0)
fmenu.add_command(label="Info", command=fileInfo, accelerator="Ctrl+I")
fmenu.add_separator()
fmenu.add_command(label="New", command=newFile, accelerator="Ctrl+N")
fmenu.add_command(label="Save", command=saveFile, accelerator="Ctrl+S")
fmenu.add_command(label="Save as", command=lambda:[saveFile(True)], accelerator="Ctrl+Shift+S")
fmenu.add_command(label="Open", command=openFile, accelerator="Ctrl+O")

rmenu = Menu(fmenu, tearoff=0)

rcf = open(dir+"/recent"+ext, "r")
rct = rcf.read().splitlines()
rcf.close()

for i in range(len(rct)):
	rmenu.add_command(label=rct[i], command=lambda r=rct[i]: openFile(r))

fmenu.add_cascade(label="Recent", menu=rmenu)

fmenu.add_separator()

emenu = Menu(fmenu, tearoff=0)
emenu.add_radiobutton(label="UTF-8", variable=enc, value='utf-8')
emenu.add_radiobutton(label="ASCII", variable=enc, value='ascii')
emenu.invoke(0)
fmenu.add_cascade(label="Encoding", menu=emenu)

fmenu.add_command(label="Quit", command=root.quit, accelerator="Alt+F4")

menu.add_cascade(label="File", menu=fmenu)

smenu = Menu(menu, tearoff=0)
smenu.add_command(label="Edit font", command=editFont, accelerator="Ctrl+F")
menu.add_cascade(label="Settings", menu=smenu)

tmenu = Menu(smenu, tearoff=0)

thf = open(dir+"/themes"+ext, "r") 
tht = thf.read().splitlines()
thf.close()

udf = open(dir+"/user"+ext, "r")
udt = udf.read().splitlines()
udf.close()

for i in range(len(udt)):
	exec(udt[i])

for i in range(len(tht)):
	if ("=" not in tht[i]):
		tx = tht[i]
		tmenu.add_radiobutton(label=tx, command=lambda t=tx:[switchTheme(t)])
		if tx == theme:
			tmenu.invoke(i)
smenu.add_cascade(label="Theme", menu=tmenu)

wmenu = Menu(menu, tearoff=0)
wmenu.add_command(label="Attach/detach menu", command=tachMenu)
wmenu.add_command(label="Fullscreen", command=lambda:[root.state('zoomed') if root.state() == "normal" else root.state("normal")], accelerator="F11")
wmenu.add_command(label="Minimize", command=lambda:[root.state('iconic') if root.state() == "normal" else root.state("normal")])
menu.add_cascade(label="Window", menu=wmenu)

hmenu = Menu(menu, tearoff=0)
hmenu.add_command(label="Help", command=openHelp, accelerator="Ctrl+H")
hmenu.add_command(label="About", command=openAbout)
menu.add_cascade(label="Help", menu=hmenu)

root.bind("<Control-+>", zoomIn)
root.bind("<Control-minus>", zoomOut)
root.bind("<Control-n>", lambda e:[newFile()])
root.bind("<Control-o>", lambda e:[openFile()])
root.bind("<Control-s>", lambda e:[saveFile()])
root.bind("<Control-S>", lambda e:[saveFile(True)])
root.bind("<Control-i>", lambda e:[fileInfo()])
root.bind("<Control-f>", lambda e:[editFont()])
root.bind("<Control-h>", lambda e:[openHelp()])
root.bind("<Control-0>", zoomNorm)
root.bind('<Button-3>', contextmenu)
root.bind("<Key>", handleKey)

if (attach):
	tachMenu()

root.geometry("{}x{}".format(wWidth, wHeight))
root.iconbitmap(icon)

app = Window(root)
switchTheme(theme)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()