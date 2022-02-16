import cv2 as cv
import numpy as np
from chibi.miru.draw import Draw
from chibi.miru.barcode import Barcode


class Image:
    def __init__( self, ndarray, name=None ):
        if isinstance( ndarray, str ):
            self.name = ndarray
            ndarray = cv.imread( ndarray, cv.IMREAD_COLOR )
        else:
            self.name = name
        self.raw = ndarray
        self.draw = Draw( self.raw )
        self.barcode = Barcode( self.gray )

    def show( self, name=None, img=None ):
        if img is None:
            img = self.raw
        if name is None:
            name = self.name
        cv.imshow( name, img )

    @property
    def gray( self ):
        try:
            return self._raw_gray
        except AttributeError:
            self._raw_gray = cv.cvtColor( self.raw, cv.COLOR_BGR2GRAY )
            return self._raw_gray
