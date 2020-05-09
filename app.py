from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showinfo
from tkinter import font
from pathlib import Path
import sys, os
import re

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
zoom	= 2
min		= 5
max		= 41
fnt		= "Segoe UI Light"
fntSys	= "Segoe UI"
theme	= "Light"
attach	= 0

dir = os.path.realpath(__file__).replace("app.py","")+"data"
ext = '.pdat'
if not (Path(dir).is_dir()):
	Path(dir).mkdir()
	files = [
		("themes","Light\ncBG=#fff\ncFG=#000\ncDark=#ddd\ncHover=#bbb\nDark\ncBG=#000\ncFG=#fff\ncDark=#222\ncHover=#444"),
		("user","")
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

def editFont():
	w = Toplevel()
	w.title("Select Font")
	w.geometry("400x400")
	
	f = list(font.families())
	f.sort(key = lambda x: x[0])
	
	fr = Frame(w, style='s.Label')
	
	fs = font.Font(family=fnt, size=txSizeD)
	
#	fss = Style()
#	fss.configure('sf.Label', foreground=cFG, background=cBG, font=fs)
	
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

def newFile():
	showinfo("window", "sup fam")

def openFile():
	showinfo("window", "sup fam")

def saveFile():
	showinfo("window", "sup fam")

def switchTheme(to):
	global cBG, cFG, cDark, cHover, theme
	
	f = open(dir+"/themes"+ext, "r") 
	t = f.read().splitlines()
	f.close()
	
	c = 0
	co = [None,None,None,None]
	for i in range(0,len(t)):
		if c > 0 and c < 5:
			co[c-1] = (t[i].split("="))[1]
			c += 1
		if (t[i] == to):
			c = 1
	if (co[0] == None):
		co = ['#fff','#000','#ddd','#bbb']
	
	cBG=co[0]
	cFG=co[1]
	cDark=co[2]
	cHover=co[3]
	
	app.e.config(selectbackground=cDark, insertbackground=cFG, bg=cBG, fg=cFG)
	app.styTx.configure('s.Label', foreground=cFG, background=cBG, font=fntSys)
	app.styBt.configure('s.TButton',foreground=cFG,background=cDark,font=(fntSys,txSizeB),relief="flat")
	app.styBt.map('s.TButton', background=[('pressed','!disabled',cHover),('active',cHover)], font=[('active',(fntSys,txSizeB))], highlightcolor=[('active','#f00')])
	app.stySc.configure('s.Horizontal.TScale',db=0,foreground='#f00',background=cFG,font=(fntSys,txSizeB),relief="flat")
	
	theme = to

def openHelp():
	w = Toplevel()
	w.title("Help")
	w.geometry("{}x{}".format(20*txSizeS,10*txSizeS))
	
	f = Frame(w, style='s.Label')
	l = Label(f, text="Shortcuts:\n\nIncrease text size: Ctrl + +\nDecrease text size: Ctrl + -", style='s.Label')
	
	l.pack(fill='x', padx=pad, pady=pad)
	f.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

def fileInfo():
	w = Toplevel()
	w.title("File information")
	w.geometry("{}x{}".format(20*txSizeS,10*txSizeS))
	
	words = str(len(re.sub(' +', ' ', app.e.get("1.0", END).replace("\n"," ")).split(" "))-1)
	chars = str(len(app.e.get("1.0", END))-1)
	schar = str(len(re.sub(' +', '', app.e.get("1.0", END).replace("\n"," "))))
	
	f = Frame(w, style='s.Label')
	l = Label(f, text="Words: "+words+"\nCharacters: "+chars+"\nWithout spaces: "+schar, style='s.Label')
	
	l.pack(fill='x', padx=pad, pady=pad)
	f.pack(anchor=N, fill=BOTH, expand=True, side=LEFT)

def tachMenu():
	if (root["menu"] == ''):
		root.config(menu=menu)
	else:
		root.config(menu='')

def on_closing():
	cont = "theme='"+theme+"'\nattach="+("0"if root["menu"]=='' else"1")+"\nfntTx.config(family='"+fntTx["family"]+"',size="+str(fntTx["size"])+")\nwWidth="+str(wWidth)+"\nwHeight="+str(wHeight)
	
	f = open(dir+"/user"+ext, "w")
	f.write(cont)
	f.close()
	
	root.destroy()

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()
		
		self.styTx = Style()
		self.styBt = Style()
		self.styBt.theme_use('clam')
		self.stySc = Style()
	
	def init_window(self):
		self.master.title("Proton Lite")
		
		self.pack(fill=BOTH, expand=1)
		
		self.e = Text(self, font=fntTx, bg=cBG, fg=cFG, tabs=5, selectbackground=cDark, insertbackground=cFG, bd=0, padx=pad, pady=pad, borderwidth=0)
		self.e.place(x=0, y=0, width=wWidth, height=wHeight)
		
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

menu = Menu(root, tearoff=0)

fmenu = Menu(menu, tearoff=0)
fmenu.add_command(label="Info", command=fileInfo)
fmenu.add_separator()
fmenu.add_command(label="New", command=newFile)
fmenu.add_command(label="Save", command=saveFile)
fmenu.add_command(label="Open", command=openFile)
fmenu.add_separator()
fmenu.add_command(label="Quit", command=root.quit)
menu.add_cascade(label="File", menu=fmenu)

smenu = Menu(menu, tearoff=0)
smenu.add_command(label="Edit font", command=editFont)
menu.add_cascade(label="Settings", menu=smenu)

tmenu = Menu(smenu, tearoff=0)

thf = open(dir+"/themes"+ext, "r") 
tht = thf.read().splitlines()
thf.close()

for i in range(0,len(tht)):
	if ("=" not in tht[i]):
		tx = tht[i]
		tmenu.add_radiobutton(label=tx, command=lambda t=tx:[switchTheme(t)])
smenu.add_cascade(label="Theme", menu=tmenu)

wmenu = Menu(menu, tearoff=0)
wmenu.add_command(label="Attach/detach menu", command=tachMenu)
menu.add_cascade(label="Window", menu=wmenu)

menu.add_command(label="Help", command=openHelp)

udf = open(dir+"/user"+ext, "r")
udt = udf.read().splitlines()
udf.close()

for i in range(len(udt)):
	exec(udt[i])

root.bind("<Control-+>", zoomIn)
root.bind("<Control-minus>", zoomOut)
root.bind("<Control-0>", zoomNorm)
root.bind('<Button-3>', contextmenu)

if (attach):
	tachMenu()

root.geometry("{}x{}".format(wWidth, wHeight))

app = Window(root)
switchTheme(theme)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()