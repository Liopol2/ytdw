from tkinter import *
from tkinter.ttk import *
import os
from pytube import *
from pytube.cli import on_progress
from icecream import ic
# Creat ing parent Tkinter window 
app = Tk() 
app.title('Youtube Downloader')

#Output Option
output=StringVar(app,'audio')
outputoptions ={
            'Audio':'audio',
            'Video':'video'
        }

#Video Quality Option
videoquality = StringVar(app,'first')
videoqualityoptions = {
            '144p':"144p",
			'240p':"240p",
			'360p':"360p",
			'480p':"480p",
			'720p':"720p",
			'highest':'first'
        }

#Audio Quality Option
audioquality = StringVar(app,'160kbps')	
audioqualityoptions = {
	'48kbps(mp4)':'48kbps',
	'50kbps(webm)':'50kbps',
	'70kbps(webm)':'70kbps',
	'128kbps(mp4)':'128kbps',
	'160kbps(webm)':'160kbps'	
}

def update_output_value():
    selected_option = output.get()

    print(f"Selected option: {selected_option}")

    if selected_option == 'video':
        for (txt, val) in videoqualityoptions.items():
            Radiobutton(app, text=txt, variable=videoquality, value=val).pack(side=TOP, ipady=4)
    elif selected_option == 'audio':
        Label(app, text='Audio Quality', font=20).pack()
        for (txt, val) in audioqualityoptions.items():
            Radiobutton(app, text=txt, variable=audioquality, value=val).pack(side=TOP, ipady=4)
#Output choice
outputlabel=Label(text='Output',font=20).pack()
videoout=Radiobutton(app, text="Audio", variable=output, value='audio', command=update_output_value).pack(side = TOP, ipady = 4) 
audioout=Radiobutton(app, text="Video", variable=output, value='video', command=update_output_value).pack(side = TOP, ipady = 4) 


#Output Folder
folder = os.path.join(os.path.expanduser('~'),'Music')
print(folder)
folderlabel=Label(text=f"Destino: {folder}",font=25).pack()

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
		downloadstream(stream)
		ic(f'{stream.title} listo en {folder}')

def downloadstream(video):
	bytes_received=0
	if output.get() == 'audio':
		aquality=audioquality.get()		
		try:
			a=video.streams.filter(only_audio=True,abr=audioquality.get())
			size=a.first().filesize
			for item in video.streams.filter(only_audio=True):
				ic(item)
			ic(a,size)
			a.first().download(output_path=folder)
			content.set(f'{video.title} Listo {audioquality.get()}')
		except Exception as e:
			ic(f'Exception al procesar audio {e}')
	elif output.get() == 'video':
		vquality=videoquality.get()		
		if vquality == 'first':
			v=video.streams.filter(progressive=True).order_by("resolution").first()
			content.set(f'descagado {video} a la mejor calidad')
			v.download(output_path=folder)
		elif vquality:			
			try:
				ic(vquality)
				v=video.streams.filter(progressive=True,res=vquality).first()
				size=v.filesize
				content.set(f'descagado {video.title} ')
				ic(f'descargando {video.title} de {size} MB.')
				v.download(output_path=folder)
			except Exception as e:
				ic({e})
				content.set(f'error con {video.title} a calidad {videoquality.get()} reintente con otra calidad')
		else:
			ic(f"se ejecuto else {videoquality.get()}")

content=StringVar(app,'Insert link here')
link = Entry(width=31, font='Arial 30',justify='center',textvariable=content)
link.bind('<1>',clearentry)
link.bind('<Key-Return>',validate_link)
link.pack()

mainloop() 