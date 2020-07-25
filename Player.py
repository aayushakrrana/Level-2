from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
pr_color="#46e2cf"
root1 = Tk()
root1.title('PlayZ')
root1.iconbitmap('logo.ico')
root1.geometry("500x330")
root1.config(bg=pr_color)
'''
root_bg=PhotoImage(file='ServQuick.jpg')
root=Label(root1,image=root_bg)
root.pack()'''
#ent = Entry(w)
#ent.pack()
#ent.focus_set()

# Initialze Pygame Mixer
pygame.mixer.init()


# Grab Song Length Time Info
def play_time():
	# Check for double timing
	if stopped:
		return
	# Grab Current Song Elapsed Time
	current_time = pygame.mixer.music.get_pos() / 1000

	# throw up temp label to get data
	#slider_label.config(text=f'Slider: {int(seek_bar.get())} and Song Pos: {int(current_time)}')
	# convert to time format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	# Get Currently Playing Song
	#current_song = song_box.curselection()
	#Grab song title from playlist
	song = song_box.get(ACTIVE)


	# add directory structure and mp3 to song title
	song = f'F:/lpt1/Gaane/{song}.mp3'
	# Load Song with Mutagen
	song_mut = MP3(song)
	# Get song Length
	global song_length
	song_length = song_mut.info.length
	# Convert to Time Format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	# Increase current time by 1 second
	current_time +=1

	if int(seek_bar.get()) == int(song_length):
		status_bar.config(text=f'-: {converted_song_length}  ::  {converted_song_length} :- ')
	elif paused:
		pass
	elif int(seek_bar.get()) == int(current_time):
		# Update Slider To position
		slider_position = int(song_length)
		seek_bar.config(to=slider_position, value=int(current_time))

	else:
		# Update Slider To position
		slider_position = int(song_length)
		seek_bar.config(to=slider_position, value=int(seek_bar.get()))

		# convert to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(seek_bar.get())))

		# Output time to status bar
		status_bar.config(text=f'-: {converted_current_time}  ::  {converted_song_length} :- ')

		# Move this thing along by one second
		next_time = int(seek_bar.get()) + 1
		seek_bar.config(value=next_time)



	# update time
	status_bar.after(1000, play_time)


#Add Song Function
def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))

	#strip out the directory info and .mp3 extension from the song name
	song = song.replace("F:/lpt1/Gaane/", "")
	song = song.replace(".mp3", "")

	# Add song to listbox
	song_box.insert(END, song)

# Add many songs to playlist
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))

	# Loop thru song list and replace directory info and mp3
	for song in songs:
		song = song.replace("F:/lpt1/Gaane/", "")
		song = song.replace(".mp3", "")
		# Insert into playlist
		song_box.insert(END, song)

# Play selected song
def play():
	# Set Stopped Variable To False So Song Can Play
	global stopped
	stopped = False
	song = song_box.get(ACTIVE)
	song = f'F:/lpt1/Gaane/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# Call the play_time function to get song length
	play_time()

	# Get current Volume
	current_volume = pygame.mixer.music.get_volume()
	# Times by 100 to make it easier to work with
	current_volume = current_volume * 100
	#slider_label.config(text=current_volume * 100)

	# Change Volume Meter Picture
	if int(current_volume) < 1:
		vol_slider.config(image=vol0)
	elif int(current_volume) > 0 and int(current_volume) <= 25:
		vol_slider.config(image=vol1)
	elif int(current_volume) >= 25 and int(current_volume) <= 50:
		vol_slider.config(image=vol2)
	elif int(current_volume) >= 50 and int(current_volume) <= 75:
		vol_slider.config(image=vol3)
	elif int(current_volume) >= 75 and int(current_volume) <= 100:
		vol_slider.config(image=vol4)


# Stop playing current song
global stopped
stopped = False
def stop():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	seek_bar.config(value=0)
	# Stop Song From Playing
	pygame.mixer.music.stop()
	song_box.selection_clear(ACTIVE)

	# Clear The Status Bar
	status_bar.config(text='')

	# Set Stop Variable To True
	global stopped
	stopped = True

	# Get current Volume
	current_volume = pygame.mixer.music.get_volume()
	# Times by 100 to make it easier to work with
	current_volume = current_volume * 100
	#slider_label.config(text=current_volume * 100)

	# Change Volume Meter Picture
	if int(current_volume) < 1:
		vol_slider.config(image=vol0)
	elif int(current_volume) > 0 and int(current_volume) <= 25:
		vol_slider.config(image=vol1)
	elif int(current_volume) >= 25 and int(current_volume) <= 50:
		vol_slider.config(image=vol2)
	elif int(current_volume) >= 50 and int(current_volume) <= 75:
		vol_slider.config(image=vol3)
	elif int(current_volume) >= 75 and int(current_volume) <= 100:
		vol_slider.config(image=vol4)

# Play The Next Song in the playlist
def next_song():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	seek_bar.config(value=0)

	# Get the current song tuple number
	next_one = song_box.curselection()
	# Add one to the current song number
	next_one = next_one[0]+1
	#Grab song title from playlist
	song = song_box.get(next_one)
	# add directory structure and mp3 to song title
	song = f'F:/lpt1/Gaane/{song}.mp3'
	# Load and play song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist listbox
	song_box.selection_clear(0, END)

	# Activate new song bar
	song_box.activate(next_one)

	# Set Active Bar to Next Song
	song_box.selection_set(next_one, last=None)

# Play Previous Song In Playlist
def previous_song():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	seek_bar.config(value=0)
	# Get the current song tuple number
	next_one = song_box.curselection()
	# Add one to the current song number
	next_one = next_one[0]-1
	#Grab song title from playlist
	song = song_box.get(next_one)
	# add directory structure and mp3 to song title
	song = f'F:/lpt1/Gaane/{song}.mp3'
	# Load and play song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist listbox
	song_box.selection_clear(0, END)

	# Activate new song bar
	song_box.activate(next_one)

	# Set Active Bar to Next Song
	song_box.selection_set(next_one, last=None)

# Delete A Song
def delete_song():
	stop()
	# Delete Currently Selected Song
	song_box.delete(ANCHOR)
	# Stop Music if it's playing
	pygame.mixer.music.stop()

# Delete All Songs from Playlist
def delete_all_songs():
	stop()
	# Delete All Songs
	song_box.delete(0, END)
	# Stop Music if it's playing
	pygame.mixer.music.stop()

# Create Global Pause Variable
global paused
paused = False

# Pause and Unpause The Current Song
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		# Unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		# Pause
		pygame.mixer.music.pause()
		paused = True

# Create slider function
def slide(x):
	#slider_label.config(text=f'{int(seek_bar.get())} of {int(song_length)}')
	song = song_box.get(ACTIVE)
	song = f'F:/lpt1/Gaane/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=int(seek_bar.get()))

# Create Volume Function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

	# Get current Volume
	current_volume = pygame.mixer.music.get_volume()
	# Times by 100 to make it easier to work with
	current_volume = current_volume * 100
	#slider_label.config(text=current_volume * 100)

	# Change Volume Meter Picture
	if int(current_volume) < 1:
		vol_slider.config(image=vol0)
	elif int(current_volume) > 0 and int(current_volume) <= 25:
		vol_slider.config(image=vol1)
	elif int(current_volume) >= 25 and int(current_volume) <= 50:
		vol_slider.config(image=vol2)
	elif int(current_volume) >= 50 and int(current_volume) <= 75:
		vol_slider.config(image=vol3)
	elif int(current_volume) >= 75 and int(current_volume) <= 100:
		vol_slider.config(image=vol4)

# Create Master Frame
master_frame = Frame(root1)
master_frame.pack(pady=(5,0))
master_frame.config(bg=pr_color)

# Create Playlist Box
song_box = Listbox(master_frame, bg="#04030f", fg="white", width=60, selectbackground="#3b3d3f", selectforeground="white")
song_box.grid(row=0, column=0)


back_btn_img = PhotoImage(file='img/control/back.png')
forward_btn_img =  PhotoImage(file='img/control/next.png')
play_btn_img =  PhotoImage(file='img/control/play.png')
pause_btn_img =  PhotoImage(file='img/control/pause.png')
stop_btn_img =  PhotoImage(file='img/control/stop.png')
delete_btn_img = PhotoImage(file='img/control/delete.png')
add_btn_img = PhotoImage(file='img/control/add.png')
# Define Volume Control Images
global vol0
global vol1
global vol2
global vol3
global vol4
vol0 =  PhotoImage(file='img/vol/Vol0.png')
vol1 =  PhotoImage(file='img/vol/Vol1.png')
vol2 =  PhotoImage(file='img/vol/Vol1.png')
vol3 =  PhotoImage(file='img/vol/Vol3.png')
vol4 =  PhotoImage(file='img/vol/Vol4.png')

# Create Player Control Frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=2, column=0, pady=20)
controls_frame.config(bg=pr_color)

# Create Volume Meter
vol_slider = Label(master_frame, image=vol0)
vol_slider.grid(row=1, column=1, padx=10)
vol_slider.config(bg=pr_color)

# Create Volume Label Frame
vol_frame = LabelFrame(master_frame, text="Volume")
vol_frame.grid(row=0, column=1, padx=30)
vol_frame.config(bg=pr_color, fg="white")

# Create Player Control Buttons
back_btn = Button(controls_frame, image=back_btn_img,bg=pr_color, borderwidth=0, command=previous_song)
forward_btn = Button(controls_frame, image=forward_btn_img,bg=pr_color, borderwidth=0, command=next_song)
play_btn = Button(controls_frame, image=play_btn_img,bg=pr_color, borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_btn_img,bg=pr_color, borderwidth=0, command=lambda: pause(paused))
stop_btn =  Button(controls_frame, image=stop_btn_img,bg=pr_color, borderwidth=0, command=stop)

add_btn = Button(controls_frame, image=add_btn_img,bg=pr_color, borderwidth=0,command=add_many_songs)
delete_btn = Button(controls_frame, image=delete_btn_img,bg=pr_color, borderwidth=0,command=delete_song)

back_btn.grid(row=2, column=0, padx=10)
forward_btn.grid(row=2, column=2, padx=10)
play_btn.grid(row=2, column=1, padx=10)
pause_btn.grid(row=2, column=3, padx=10)
stop_btn.grid(row=2, column=4, padx=10)

add_btn.grid(row=2,column=7,padx=10)
delete_btn.grid(row=2,column=8,padx=10)
# Create Menu
my_menu = Menu(root1)
root1.config(menu=my_menu)

# Create Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
# Add Many Songs to playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)


# Create Status Bar
status_bar = Label(root1, text='Stopped', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create Music Position Slider
seek_bar = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
seek_bar.grid(row=1, column=0, pady=(20,0))


# Create Volume Slider
volume_slider = ttk.Scale(vol_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)
#volume_slider.configure(background=pr_color)


# Create Temporary Slider Label
#slider_label = Label(root, text="0")
#slider_label.pack(pady=10)

root1.mainloop()
