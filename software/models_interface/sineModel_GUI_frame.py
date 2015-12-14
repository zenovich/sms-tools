# GUI frame for the sineModel_function.py

from Tkinter import *
import tkFileDialog, tkMessageBox
import sys, os
from scipy.io.wavfile import read
import sineModel_function
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/'))
import utilFunctions as UF

class SineModel_frame:

	def __init__(self, parent):
		self.parent = parent
		self.canvas = Canvas(self.parent)
		self.frame = Frame(self.canvas)
		self.scrollbar = Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.scrollbar.set)
		self.scrollbar.pack(side="right", fill=Y)
		self.canvas.pack(side="left", fill="both", expand=YES)
		self.frame.pack(side="left", fill="both", expand=YES)
		self.canvas.create_window((4,4), window=self.frame, anchor="nw")
		self.frame.bind("<Configure>", self.onFrameConfigure)
		self.initUI()

	def onFrameConfigure(self, event):
		'''Reset the scroll region to encompass the inner frame'''
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		size = (self.parent.winfo_reqwidth(), self.parent.winfo_reqheight())
		self.canvas.config(scrollregion="0 0 %s %s" % size)
		self.canvas.config(width=event.width, height=event.height)


	def initUI(self):

		choose_label = "Input file (.wav, mono and 44100 sampling rate):"
		Label(self.frame, text=choose_label).grid(row=0, column=0, sticky=W, padx=5, pady=(10,2))

		#TEXTBOX TO PRINT PATH OF THE SOUND FILE
		self.filelocation = Entry(self.frame)
		self.filelocation.focus_set()
		self.filelocation["width"] = 25
		self.filelocation.grid(row=1,column=0, sticky=W, padx=10)
		self.filelocation.delete(0, END)
		self.filelocation.insert(0, '../../sounds/bendir.wav')

		#BUTTON TO BROWSE SOUND FILE
		self.open_file = Button(self.frame, text="Browse...", command=self.browse_file) #see: def browse_file(self)
		self.open_file.grid(row=1, column=0, sticky=W, padx=(220, 6)) #put it beside the filelocation textbox

		#BUTTON TO PREVIEW SOUND FILE
		self.preview = Button(self.frame, text=">", command=lambda:UF.wavplay(self.filelocation.get()), bg="gray30", fg="white")
		self.preview.grid(row=1, column=0, sticky=W, padx=(306,6))

		## SINE MODEL

		#ANALYSIS WINDOW TYPE
		wtype_label = "Window type:"
		Label(self.frame, text=wtype_label).grid(row=2, column=0, sticky=W, padx=5, pady=(10,2))
		self.w_type = StringVar()
		self.w_type.set("hamming") # initial value
		window_option = OptionMenu(self.frame, self.w_type, "rectangular", "hanning", "hamming", "blackman", "blackmanharris")
		window_option.grid(row=2, column=0, sticky=W, padx=(95,5), pady=(10,2))

		self.bandsframe = LabelFrame(self.frame, text='Bands')
		self.bandsframe.grid(row=3, column=0, sticky=W, padx=5, pady=(10,2))

		self.bandsframe.bands = []
		self.add_band()

		self.bandplus = Button(self.frame, justify=RIGHT, text="Add band", command=lambda:self.add_band())
		self.bandplus.grid(sticky=W, padx=5, pady=(10,2))

		#THRESHOLD MAGNITUDE
		t_label = "Magnitude threshold (t) (in dB):"
		Label(self.frame, text=t_label).grid(row=5, column=0, sticky=W, padx=5, pady=(10,2))
		self.t = Entry(self.frame, justify=CENTER)
		self.t["width"] = 5
		self.t.grid(row=5, column=0, sticky=W, padx=(205,5), pady=(10,2))
		self.t.delete(0, END)
		self.t.insert(0, "-80")

		#MIN DURATION SINUSOIDAL TRACKS
		minSineDur_label = "Minimum duration of sinusoidal tracks:"
		Label(self.frame, text=minSineDur_label).grid(row=6, column=0, sticky=W, padx=5, pady=(10,2))
		self.minSineDur = Entry(self.frame, justify=CENTER)
		self.minSineDur["width"] = 5
		self.minSineDur.grid(row=6, column=0, sticky=W, padx=(250,5), pady=(10,2))
		self.minSineDur.delete(0, END)
		self.minSineDur.insert(0, "0.02")

		#MAX NUMBER PARALLEL SINUSOIDS
		maxnSines_label = "Maximum number of parallel sinusoids:"
		Label(self.frame, text=maxnSines_label).grid(row=7, column=0, sticky=W, padx=5, pady=(10,2))
		self.maxnSines = Entry(self.frame, justify=CENTER)
		self.maxnSines["width"] = 5
		self.maxnSines.grid(row=7, column=0, sticky=W, padx=(250,5), pady=(10,2))
		self.maxnSines.delete(0, END)
		self.maxnSines.insert(0, "150")

		#FREQUENCY DEVIATION ALLOWED
		freqDevOffset_label = "Max frequency deviation in sinusoidal tracks (at freq 0):"
		Label(self.frame, text=freqDevOffset_label).grid(row=8, column=0, sticky=W, padx=5, pady=(10,2))
		self.freqDevOffset = Entry(self.frame, justify=CENTER)
		self.freqDevOffset["width"] = 5
		self.freqDevOffset.grid(row=8, column=0, sticky=W, padx=(350,5), pady=(10,2))
		self.freqDevOffset.delete(0, END)
		self.freqDevOffset.insert(0, "10")

		#SLOPE OF THE FREQ DEVIATION
		freqDevSlope_label = "Slope of the frequency deviation (as function of freq):"
		Label(self.frame, text=freqDevSlope_label).grid(row=9, column=0, sticky=W, padx=5, pady=(10,2))
		self.freqDevSlope = Entry(self.frame, justify=CENTER)
		self.freqDevSlope["width"] = 5
		self.freqDevSlope.grid(row=9, column=0, sticky=W, padx=(340,5), pady=(10,2))
		self.freqDevSlope.delete(0, END)
		self.freqDevSlope.insert(0, "0.001")

		#BUTTON TO COMPUTE EVERYTHING
		self.compute = Button(self.frame, text="Compute", command=self.compute_model, bg="dark red", fg="white")
		self.compute.grid(row=10, column=0, padx=5, pady=(10,2), sticky=W)


		#BUTTON TO PLAY OUTPUT
		output_label = "Output:"
		Label(self.frame, text=output_label).grid(row=11, column=0, sticky=W, padx=5, pady=(10,15))
		self.output = Button(self.frame, text=">", command=lambda:UF.wavplay('output_sounds/' + os.path.basename(self.filelocation.get())[:-4] + '_sineModel.wav'), bg="gray30", fg="white")
		self.output.grid(row=11, column=0, padx=(60,5), pady=(10,15), sticky=W)

		# define options for opening file

		self.file_opt = options = {}
		options['defaultextension'] = '.wav'
		options['filetypes'] = [('All files', '.*'), ('Wav files', '.wav')]
		options['initialdir'] = '../../sounds/'
		options['title'] = 'Open a mono audio file .wav with sample frequency 44100 Hz'

	def browse_file(self):

		self.filename = tkFileDialog.askopenfilename(**self.file_opt)

		#set the text of the self.filelocation
		self.filelocation.delete(0, END)
		self.filelocation.insert(0,self.filename)

	def compute_model(self):

		try:
			inputFile = self.filelocation.get()
			window = self.w_type.get()
			reversedBands = self.bandsframe.winfo_children()
			b = []
			M = []
			N = []
			for bandNum in xrange(len(reversedBands)):
				band = reversedBands[bandNum]
				M.append(int(band.M.get()))
				N.append(int(band.N.get()))
				b.append(int(band.B.get()))
			t = int(self.t.get())
			minSineDur = float(self.minSineDur.get())
			maxnSines = int(self.maxnSines.get())
			freqDevOffset = int(self.freqDevOffset.get())
			freqDevSlope = float(self.freqDevSlope.get())

			sineModel_function.main(inputFile, window, M, N, t, minSineDur, maxnSines, freqDevOffset, freqDevSlope, b)

		except ValueError as errorMessage:
			tkMessageBox.showerror("Input values error", errorMessage)

	def add_band(self):
		BAND_frame = LabelFrame(self.bandsframe)
		BAND_frame.grid(sticky=W, padx=5, pady=(0,0))

		#WINDOW SIZE
		M_label = "Window size (M):"
		Label(BAND_frame, text=M_label).grid(row=0, column=0, sticky=W, padx=5, pady=(10,2))
		M_entry = Entry(BAND_frame, justify=CENTER)
		M_entry["width"] = 5
		M_entry.grid(row=0, column=0, sticky=W, padx=(115,5), pady=(10,2))
		M_entry.delete(0, END)
		M_entry.insert(0, "2001")
		BAND_frame.M = M_entry

		#FFT SIZE
		N_label = "FFT size (N) (power of two bigger than M):"
		N_entry = Label(BAND_frame, text=N_label).grid(row=1, column=0, sticky=W, padx=5, pady=(10,2))
		N_entry = Entry(BAND_frame, justify=CENTER)
		N_entry["width"] = 5
		N_entry.grid(row=1, column=0, sticky=W, padx=(270,5), pady=(10,2))
		N_entry.delete(0, END)
		N_entry.insert(0, "2048")
		BAND_frame.N = N_entry

		#Band right limit
		B_label = "Band right limit (b):"
		B_entry = Label(BAND_frame, text=B_label).grid(row=2, column=0, sticky=W, padx=5, pady=(10,2))
		B_entry = Entry(BAND_frame, justify=CENTER)
		B_entry["width"] = 5
		B_entry.grid(row=2, column=0, sticky=W, padx=(270,5), pady=(10,2))
		B_entry.delete(0, END)
		BAND_frame.B = B_entry

		if len(self.bandsframe.bands) > 0:
			#'Remove' button
			REM_button = Button(BAND_frame, text='X', command=lambda:{BAND_frame.grid_forget(), BAND_frame.destroy()})
			REM_button.grid(row=0, column=0, sticky='NE', padx=5, pady=(10,2))
			BAND_frame.REM_button = REM_button

		self.bandsframe.bands.append(BAND_frame)
