import tkinter
from tkinter import  ttk
from pytube import YouTube
import threading


def progress_func(stream, data_chunk, bytes_remaining):
    global remaining_size
    progress = (stream.filesize-bytes_remaining)/stream.filesize
    progress_percentage = int(progress*100)
    lb_dummy2.config(text=f"{progress_percentage}% Completed")
    remaining_size = bytes_remaining
    print(progress_percentage)
    progress_bar['value'] = progress_percentage
    window.update_idletasks()
def complete_func(stream,file_path):
    print("File downloaded")
def download(link):
    yt = YouTube(link
                ,on_progress_callback=progress_func,
                on_complete_callback=complete_func,
                use_oauth=False,
                allow_oauth_cache=True
            )
    return [yt.streams.filter(progressive=True),yt.title]


streams = list()

def list_streams(*args):
    global streams
    streams = download(txt_link.get())
    print(streams)
    lb_vid_title.config(text=streams[1])
    reso_list = [stream.resolution for stream in streams[0]]
    combo_stream["values"]=reso_list

def download_video():
    for stream in streams[0]:
        if(combo_stream.get()==stream.resolution):
            stream.download()


def initialization_stream():
    lb_vid_title.config(text="Loading Data...")
    threading.Thread(target=list_streams).start()

def initialization_download():
    lb_dummy.config(text="Initiating Download")
    threading.Thread(target=download_video).start()

window = tkinter.Tk()
window.title("My Review Youtube Downloader")
window.grid()

lb_title = tkinter.Label(window, text="My Review Youtube Downloader").grid(column=0,row=0)

txt_link = tkinter.Entry(window,width=60)
txt_link.grid(column=0,row=1)

btn_stream = ttk.Button(window,text="List Streams",command=initialization_stream).grid(column=1,row=1)

lb_vid_title = tkinter.Label(window, text="")
lb_vid_title.grid(column=0,row=2)

combo_stream = ttk.Combobox(window,width=40)
combo_stream["values"]=("Select")
combo_stream.current(0)
combo_stream.grid(column=0,row=3)

btn_download = ttk.Button(window,text="Download",command=initialization_download).grid(column=1,row=3)

lb_dummy = tkinter.Label(window, text="")
lb_dummy.grid(column=0,row=4)


progress_bar = ttk.Progressbar(window,orient="horizontal",mode="determinate",length=300)
progress_bar.grid(column=0,row=5)

lb_dummy2 = tkinter.Label(window, text="")
lb_dummy2.grid(column=0,row=6)

btn_exit = ttk.Button(window, text="Quit", command=window.destroy).grid(column=0, row=7)


window.mainloop()
