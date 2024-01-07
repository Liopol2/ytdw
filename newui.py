import re
from tkinter import *
from tkinter import ttk
import os
from tkinter import filedialog
from pytube import *
from pytube.cli import on_progress
from icecream import ic
# Creating parent Tkinter window 
app = Tk() 
app.title('Youtube Downloader')
app.iconbitmap('YoutubeDownloader.ico')

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
	ic(out)
	if out == 'Video':
		qualitybox.config(value=videoqualityoptions)
		qualitybox.current(5)  
	elif out == 'Audio':
		qualitybox.config(value=audioqualityoptions)
		qualitybox.current(4)
  
#Output choice
outputlabel=Label(text='Output',font=20).pack()
outputbox=ttk.Combobox(app,value=outputoptions)
outputbox.current(0)
outputbox.pack(pady=20)
outputbox.bind("<<ComboboxSelected>>",select_output)
Label(app, text='Quality', font=20).pack()
qualitybox=ttk.Combobox(app,value=audioqualityoptions)
qualitybox.current(4)
qualitybox.pack(pady=20)


#Output Folder
folder = os.path.join(os.path.expanduser('~'),'Music')
def cambiardestino(e):   
	global folder
	newfolder=filedialog.askdirectory(initialdir = folder,title="Seleccione una Carpeta:")
	if newfolder:
		folder = newfolder
		folderlabel.config(text=f"Destino: {folder}",font=25)
  
folderlabel=Label(text=f"Destino: {folder}",font=25)
folderlabel.bind('<1>',cambiardestino)
folderlabel.pack()
#Link
def clearentry(event):
	link.config(foreground='black')
	content.set('')
	
def validate_link(event):
	url= content.get()
	link.config(foreground='blue')
	#manage playlist
	if 'playlist' in url:
		playlist=Playlist(url)
		for stream in playlist.videos:
			stream.register_on_progress_callback(on_progress)
			ic(f'descargando {stream.title} de {playlist.title}')
			downloadstream(stream) 
	#If this is only 1 video
	else:
		stream=YouTube(url)
		ic(f'Video: {stream.title}')
		downloadstream(stream)

def downloadstream(video):
	bytes_received=0
	quality=qualitybox.get()	
	output=outputbox.get()
	if output == 'Audio':
		qualityval = re.sub(r'\([^)]*\)', '', quality)
		ic(qualityval)
		a=video.streams.filter(only_audio=True,abr=qualityval)
		if a:
			a.first().download(output_path=folder)
			content.set(f'{video.title} {qualityval} ✔')
			link.config(foreground='green')
		else: 
			content.set(f'Intente con calidad distinta a {quality}')
			link.config(foreground='red')
	elif output == 'Video':
		if quality == 'Highest':
			v=video.streams.filter(progressive=True).order_by("resolution").first()
			content.set(f'descagado {video} a la mejor calidad')
			v.download(output_path=folder)
			link.config(foreground='green')
		elif quality:			
				v=video.streams.filter(progressive=True,res=quality).first()
				ic(video,video.streams.filter(progressive=True))
				if v:
					v.download(output_path=folder)
					content.set(f'{video.title} {quality} ✔')
					link.config()
				else:
					content.set(f'Intente con calidad distinta a {quality}')
					link.config(foreground='red')

content=StringVar(app,'Insert link here')
link = Entry(width=31, font='Arial 30',justify='center',textvariable=content)
link.bind('<1>',clearentry)
link.bind('<Key-Return>',validate_link)
link.pack()

mainloop() 