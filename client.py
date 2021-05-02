#!/usr/bin/python3

import argparse
import os
import scipy.io.wavfile as wav
import sys

import satellite.apt.lib as sal

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='APT file decoder.')

	parser.add_argument("-s", "--signal", help="Plot signal.", action="store_true")
	parser.add_argument("-i", "--image", help="Decode to image.", action="store_true")
	parser.add_argument("-f", "--file", help="Audio file to process.", type=str)
	parser.add_argument("-o", "--optimized", help="Speed up image processing.", action="store_true")

	args = parser.parse_args()

	if args.file == None:
		print("File argument is required.")
		sys.exit(-1)

	if not os.path.isfile(args.file):
		print(f"{args.file} not found.")
		sys.exit(-1)

	fs, data = wav.read(args.file)

	if args.signal:
		data_crop = data[20*fs:21*fs]

		sal.plot_signal(data_crop)

	if args.image:
		if args.optimized:
			fs, data = sal.resample(fs, data)

		data_am = sal.hilbert(data)

		image = sal.build_image(fs, data_am)

		sal.plot_image(image)
