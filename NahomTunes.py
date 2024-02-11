import os
import pygame
import tkinter as tk
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("NahomTunes")
        self.root.geometry("100000000000000x10000000000000")

        self.playlist = []
        self.current_track = 0
        self.paused = False

        pygame.init()
        pygame.mixer.init()

        self.create_widgets()
        self.load_music()

    def create_widgets(self):
        self.heading_label = tk.Label(self.root, text="Welcome to NahomTunes!", font=("Garamond", 24, "bold"), pady=10, bg="#34495E", fg="Gray")
        self.heading_label.pack(fill=tk.X)

        self.listbox_frame = tk.Frame(self.root, padx=20, pady=10)
        self.listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.listbox_frame, width=40, height=15, font=("Garamond", 10), bg="#D5DBDB")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.listbox_scroll = tk.Scrollbar(self.listbox_frame)
        self.listbox_scroll.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.listbox.config(yscrollcommand=self.listbox_scroll.set)
        self.listbox_scroll.config(command=self.listbox.yview)

        self.controls_frame = tk.Frame(self.root, pady=10)
        self.controls_frame.pack()

        self.prev_button = tk.Button(self.controls_frame, text="Previous", command=self.previous_track, bg="#3498DB", fg="white", padx=10)
        self.prev_button.grid(row=0, column=0, padx=10)

        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play_music, bg="#2ECC71", fg="white", padx=10)
        self.play_button.grid(row=0, column=1, padx=10)

        self.pause_button = tk.Button(self.controls_frame, text="Pause", command=self.pause_music, bg="#F4D03F", fg="white", padx=10)
        self.pause_button.grid(row=0, column=2, padx=10)

        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop_music, bg="#E74C3C", fg="white", padx=10)
        self.stop_button.grid(row=0, column=3, padx=10)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.next_track, bg="#3498DB", fg="white", padx=10)
        self.next_button.grid(row=0, column=4, padx=10)

        self.add_song_button = tk.Button(self.root, text="Add Song", command=self.add_song, bg="#3498DB", fg="white", padx=10)
        self.add_song_button.pack(pady=10, fill=tk.X)

        self.volume_label = tk.Label(self.root, text="Volume", bg="#34495E", fg="white")
        self.volume_label.pack()

        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack()

        self.song_info_label = tk.Label(self.root, text="", bg="#34495E", fg="white")
        self.song_info_label.pack()

        self.current_time_label = tk.Label(self.root, text="", bg="#34495E", fg="white")
        self.current_time_label.pack()

    def load_music(self):
        directory = filedialog.askdirectory()
        if directory:
            for file in os.listdir(directory):
                if file.endswith(".mp3"):
                    self.playlist.append(os.path.join(directory, file))
                    self.listbox.insert(tk.END, file)

    def add_song(self):
        song = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if song:
            self.playlist.append(song)
            self.listbox.insert(tk.END, os.path.basename(song))

    def play_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            if self.playlist:
                pygame.mixer.music.load(self.playlist[self.current_track])
                pygame.mixer.music.play()
                self.root.title("NahomTunes - " + os.path.basename(self.playlist[self.current_track]))
                self.update_song_info()

    def pause_music(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.paused = False
        self.song_info_label.config(text="")
        self.current_time_label.config(text="")

    def next_track(self):
        if self.playlist:
            self.current_track = (self.current_track + 1) % len(self.playlist)
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.root.title("NahomTunes - " + os.path.basename(self.playlist[self.current_track]))
            self.update_song_info()

    def previous_track(self):
        if self.playlist:
            self.current_track = (self.current_track - 1) % len(self.playlist)
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.root.title("NahomTunes - " + os.path.basename(self.playlist[self.current_track]))
            self.update_song_info()

    def set_volume(self, val):
        volume = int(val) / 100
        pygame.mixer.music.set_volume(volume)

    def update_song_info(self):
        tags = pygame.mixer.Sound(self.playlist[self.current_track]).tags
        song_info = f"Now Playing: {tags.get('title', 'Unknown')} - {tags.get('artist', 'Unknown')}"
        self.song_info_label.config(text=song_info)

        self.current_time_label.after(1000, self.update_current_time)

    def update_current_time(self):
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() // 1000
            formatted_time = f"Time: {current_time // 60}:{current_time % 60:02d}"
            self.current_time_label.config(text=formatted_time)
            self.current_time_label.after(1000, self.update_current_time)
        else:
            self.current_time_label.config(text="")

    def start(self):
        self.root.mainloop()

# Create the main window
root = tk.Tk()
app = MusicPlayer(root)
app.start()