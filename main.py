#!/usr/bin/env python3

from chibi.miru.cam import Chibi_cam
import cv2 as cv
cam = Chibi_cam()
while True:
    f = cam.read
    if f.barcode.barcodes:
        for q in f.barcode.barcodes:
            print( q )
            f.draw.barcode_boundary( q, (255,0,0), 3 )
    f.show()
    if cv.waitKey(1) & 0xFF == ord( 'q' ):
        break
