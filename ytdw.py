#En caso de querer compilar tus propios binarios instalar pyinstaler ($pip install pyinstaller) 
#Y escriba $ pyinstaller -F -w --icon=YoutubeDownloader.ico ytdw.py en su consola preferida, para compilar.
from tkinter import *
from tkinter import ttk,filedialog
import os,re
from pytube import YouTube,Playlist

#icecream es opcional, solo se esta usando para debuggear.
from icecream import ic

# Creating parent Tkinter window 
app = Tk() 
app.title('Youtube Downloader')
app.config(bg='black')

#En caso de querer compilar este programa con pyinstaller comente la siguiente linea o incluya en el mismo directorio del ejecutable YoutubeDownloader.ico
#app.iconbitmap('YoutubeDownloader.ico')

#nada por ahora 
Transcriptoptions=[
	
]
#Video Quality Options
videoqualityoptions = [
            '144p',
			'240p',
			'360p',
			'480p',
			'720p',
			'Highest'
]

#Audio Quality Options
audioqualityoptions = [
	'48kbps(mp4)',
	'50kbps(webm)',
	'70kbps(webm)',
	'128kbps(mp4)',
	'160kbps(webm)'
]
#Output Options
outputoptions = [
	'Audio',
	'Video',
	'Transcript'
]
	
def select_output(event):
	out=outputbox.get()
	#ic(out)
	match out:
		case 'Video' :
			qualitybox.config(value=videoqualityoptions)
			qualitybox.current(5)  
		case 'Audio':
			qualitybox.config(value=audioqualityoptions)
			qualitybox.current(4)
		case 'Transcript':
			qualitybox.config(value=Transcriptoptions)


#Output choice
outputlabel=Label(text='Output',font=20).grid(row=0, column=0, padx=10, pady=5, sticky="NESW")
outputbox=ttk.Combobox(app,value=outputoptions)
outputbox.current(0)
outputbox.grid(row=0, column=1, padx=10, pady=5, sticky="NESW")
outputbox.bind("<<ComboboxSelected>>",select_output)

#Quality Option
Label(app, text='Quality', font=20).grid(row=1, column=0, padx=10, pady=5, sticky="NESW")
qualitybox=ttk.Combobox(app,value=audioqualityoptions)
qualitybox.current(4)
qualitybox.grid(row=1, column=1, padx=10, pady=5, sticky="NESW")


#Output Folder
folder = os.path.join(os.path.expanduser('~'),'Music')
def cambiardestino(e):   
	global folder
	newfolder=filedialog.askdirectory(initialdir = folder,title="Seleccione una Carpeta:")
	if newfolder:
		folder = newfolder
		folderlabel.config(text=f"📁 {folder}",font=25)
  
folderlabel=Label(text=f"📁 {folder}",font=25,cursor="hand1")
folderlabel.bind('<1>',cambiardestino)
folderlabel.grid(row=2, column=0,columnspan=2, padx=10, pady=5, sticky="NESW")

#Link
def clearentry(event):
	link.config(fg='white')
	content.set('')
	
def validate_link(event):
	url= content.get()
	link.config(foreground='blue')
	#manage playlist
	if 'playlist' in url:
		playlist=Playlist(url)
		for stream in playlist.videos:
			video= YouTube(stream.watch_url,on_progress_callback=on_progress)
			getstream(video) 
	#If this is only 1 video
	else:
		stream=YouTube(url,on_progress_callback=on_progress)
		getstream(stream)

#Progressbar method
def on_progress(stream,chunk,bytes_remaining):
	total_size = stream.filesize
	bytes_downloaded = total_size - bytes_remaining
	percentage= bytes_downloaded/ total_size * 100
	pb['value']=percentage

def fileexist(filename):
	content.set(f'{filename} ya existe')
	link.config(fg='yellow')
	link.config(bg='black')

def downloadstream(title,stream,quality="Best Quality"):
	stream.download(output_path=folder)
	content.set(f'{title} {quality} ✔')
	link.config(foreground='green')

def getstream(video):
	quality=qualitybox.get()	
	output=outputbox.get()
	title=video.title
	match output:
		case 'Audio':
			if os.path.exists(f'{folder}/{video.title}.webm'): #save folder 
				fileexist(title)
			else:
				#este regex quita lo que esta dentro del parentesis
				qualityval = re.sub(r'\([^)]*\)', '', quality)
				#ic(qualityval)
				stream = video.streams.filter(only_audio=True,abr=qualityval).first()
				if stream:      
					downloadstream(title,stream,qualityval)
				else: 
					content.set(f'Intente con calidad distinta a {quality}')
					link.config(foreground='red')
	
		case 'Video':
			if os.path.exists(f'{folder}/{video.title}.mp4'):
				fileexist(title)
			else:
				if quality == 'Highest':
					stream=video.streams.get_highest_resolution() 
					downloadstream(title,stream)
				elif quality:
					#No entiendo porque pero esto tiene que estar en dos lineas. 			
					v=video.streams.filter(progressive=True,res=quality)
					stream=v.first()
					downloadstream(title,stream,quality)
				else:
					content.set(f'Intente con calidad distinta a {quality}')
					link.config(foreground='red')
     
content=StringVar(app,'Insert link here')
link = Entry(width=31, font='Arial 30',justify='center',textvariable=content)
link.config(bg='grey',fg='white')
link.bind('<1>',clearentry)
link.bind('<Key-Return>',validate_link)
link.grid(row=3, column=0,columnspan=2, padx=10, pady=5, sticky="NESW")

#Progressbar
pb = ttk.Progressbar(
    app,
    orient='horizontal',
    mode='determinate',
    length=280
)

pb.grid(column=0, row=4, columnspan=2, padx=10, pady=5,sticky="NESW")

app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_rowconfigure(3, weight=1)
app.grid_rowconfigure(4, weight=1)
mainloop() 