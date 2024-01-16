#En caso de querer compilar tus propios binarios instalar pyinstaler ($pip install pyinstaller) 
#Y escriba $ pyinstaller -F -w --icon=YoutubeDownloader.ico ytdw.py en su consola preferida, para compilar.
from tkinter import *
from tkinter import ttk,filedialog
import os,re
from pytube import *
from pytube.cli import on_progress

#icecream es opcional, solo se esta usando para debuggear.
#from icecream import ic

# Creating parent Tkinter window 
app = Tk() 
app.title('Youtube Downloader')
app.config(bg='black')

#En caso de querer compilar este programa con pyinstaller comente la siguiente linea o incluya en el mismo directorio del ejecutable YoutubeDownloader.ico
#app.iconbitmap('YoutubeDownloader.ico')

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
	'Video'
]
	
def select_output(event):
	out=outputbox.get()
	#ic(out)
	if out == 'Video':
		qualitybox.config(value=videoqualityoptions)
		qualitybox.current(5)  
	elif out == 'Audio':
		qualitybox.config(value=audioqualityoptions)
		qualitybox.current(4)
  
#Output choice
outputlabel=Label(text='Output',font=20).grid(row=0, column=0, padx=10, pady=5, sticky="NESW")#.pack()
outputbox=ttk.Combobox(app,value=outputoptions)
outputbox.current(0)
outputbox.grid(row=0, column=1, padx=10, pady=5, sticky="NESW")#.pack(pady=20)
outputbox.bind("<<ComboboxSelected>>",select_output)

#Quality Option
Label(app, text='Quality', font=20).grid(row=1, column=0, padx=10, pady=5, sticky="NESW")#.pack()
qualitybox=ttk.Combobox(app,value=audioqualityoptions)
qualitybox.current(4)
qualitybox.grid(row=1, column=1, padx=10, pady=5, sticky="NESW")#.pack(pady=20)


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
folderlabel.grid(row=2, column=0,columnspan=2, padx=10, pady=5, sticky="NESW")#.pack()
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
			stream.register_on_progress_callback(on_progress)
			#ic(f'descargando {stream.title} de {playlist.title}')
			downloadstream(stream) 
		link.config(fg='green')
		content.set(f'{playlist.title} ✔')
	#If this is only 1 video
	else:
		stream=YouTube(url)
		#ic(f'Video: {stream.title}')
		downloadstream(stream)

def downloadstream(video):
	bytes_received=0
	quality=qualitybox.get()	
	output=outputbox.get()
	if output == 'Audio':
		if os.path.exists(f'{folder}/{video.title}.webm'):
			content.set(f'{video.title} ya existe')
			link.config(fg='yellow')
			link.config(bg='black')
		else:
			#este regex quita lo que esta dentro del parentesis
			qualityval = re.sub(r'\([^)]*\)', '', quality)
			#ic(qualityval)
			a=video.streams.filter(only_audio=True,abr=qualityval)
			if a:      
				a.first().download(output_path=folder)
				content.set(f'{video.title} {qualityval} ✔')
				link.config(foreground='green')
			else: 
				content.set(f'Intente con calidad distinta a {quality}')
				link.config(foreground='red')
	elif output == 'Video':
		if os.path.exists(f'{folder}/{video.title}.mp4'):
			content.set(f'{video.title} ya existe')
			link.config(fg='yellow')
		else:
			if quality == 'Highest':
				v=video.streams.filter(progressive=True).order_by("resolution").first()
				content.set(f'descagado {video} a la mejor calidad')
				v.download(output_path=folder)
				link.config(foreground='green')
			elif quality:			
					v=video.streams.filter(progressive=True,res=quality).first()
					filename=f'{video.title}.webm'
					#ic(video,filename)
					if v:
						if filename in folder:						
							content.set(f'⬇ {video.title}')
						v.download(output_path=folder)
						content.set(f'{video.title} {quality} ✔')
						link.config()
					else:
						content.set(f'Intente con calidad distinta a {quality}')
						link.config(foreground='red')
     
content=StringVar(app,'Insert link here')
link = Entry(width=31, font='Arial 30',justify='center',textvariable=content)
link.config(bg='grey',fg='white')
link.bind('<1>',clearentry)
link.bind('<Key-Return>',validate_link)
link.grid(row=3, column=0,columnspan=2, padx=10, pady=5, sticky="NESW")#.pack()
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
mainloop() 