#!/bin/env python3

import os
import sys
import PIL.Image

class OrderImage:
	_DateTimeOriginal = 36867
	_ImageList = []

	def _OpenImageFile(self, name):
		### Open the image file with PIL. ###
		return PIL.Image.open(name)

	def _ReadImageMeta(self, img):
		### Read the image files EXIF with PIL. ###
		return img._getexif()

	def _GetDateTimeOriginal(self, exif):
		### Get the image's original datetime in the EXIF. ###
		return exif[self._DateTimeOriginal]

	def _CloseImageFile(self, img):
		### Close the opened image file. ###
		img.close()

	def AddImage(self, name):
		### Add an image's name and meta into the list. ###
		img = self._OpenImageFile(name)
		exif = self._ReadImageMeta(img)
		t = self._GetDateTimeOriginal(exif)
		self._CloseImageFile(img)
		path, fname = os.path.split(name)
		self._ImageList.append({"Path":path, "Name":fname, "DateTimeOriginal":t})

	def OrderbyDateTimeOriginal(self):
		### Order the images in the list by their original datetime. ###
		tmp = sorted(self._ImageList, key = lambda img : img["DateTimeOriginal"])
		self._ImageList = tmp
		return self._ImageList

	def NewNamebyOrder(self):
		### Append the order number as the prefix of the file name. ###
		n = len(self._ImageList)
		d = len("{0}".format(n))

		prefix = "{0:"+"0{0}".format(d)+"d}_"

		for i in range(n):
			e = self._ImageList[i]
			e["NewName"] = prefix.format(i) + e["Name"]

	def RenamewithNewName(self):
		### Rename the real image file with the new name in the list. ###
		for e in self._ImageList:
			if e["Path"] != "":
				os.rename(e["Path"] + "/" + e["Name"], e["Path"] + "/" + e["NewName"])
			else:
				os.rename(e["Name"], e["NewName"])

if __name__ == "__main__":
	print(sys.argv)

	oi = OrderImage()

	# Add images gotten from arguments into the proccesing list.
	for name in sys.argv[1:]:
		oi.AddImage(name)

	print(oi._ImageList)

	for e in oi._ImageList:
		print("{0},\t{1}".format(e["Name"], e["DateTimeOriginal"]))

	# Order the images in the list by their Original DateTime.
	a = oi.OrderbyDateTimeOriginal()

	print("---------------------------------------")

	for e in a:
		print("{0},\t{1}".format(e["Name"], e["DateTimeOriginal"]))

	# Have the new name with the ordered list, which will be add prefix with the order number.
	oi.NewNamebyOrder()

	print("---------------------------------------")

	for e in a:
		print("{0},\t{1},\t{2}".format(e["Name"], e["DateTimeOriginal"], e["NewName"]))

	# Rename the images with their new names which were produced by pre-step.
	oi.RenamewithNewName()
