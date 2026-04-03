import functools
import io
import logging

import cv2 as cv
from PIL.Image import Image as PIL_image
from chibi.file import Chibi_path
from chibi.madness.string import generate_b64_unsecure

from chibi_miru.snippets import pil_to_cv
from chibi_miru.image import Image


class Processed( Image ):
    def __init__( self, *args, origin, **kw ):
        super().__init__( *args, origin=origin, **kw )


class Resize( Processed ):
    def __init__( self, *args, dimensions=None, **kw ):
        if dimensions is not None:
            name = f"resize_{dimensions[0]}x{dimensions[1]}"
            super().__init__( *args, name=name, **kw )
        else:
            name = None
            super().__init__( *args, **kw )
        self.dimentions = dimensions


class Threshold( Processed ):
    def __init__( self, *args, threshold_value, **kw ):
        super().__init__( *args, **kw )
        self.threshold_value = threshold_value


class Binary( Threshold ):
    def __init__( self, *args, a, b, **kw ):
        name = f"binary_{a}_{b}"
        super().__init__( *args, name=name, **kw )
        self.a = a
        self.b = b


class Dilate( Processed ):
    def __init__( self, *args, kernel, **kw ):
        super().__init__( *args, **kw )
        self.kernel = kernel


class Contours( Processed ):
    def __init__( self, *args, contours, hierarchy, **kw ):
        super().__init__( *args, **kw )
        self.contours = contours
        self.hierarchy = hierarchy
        cv.drawContours(
            self.raw, contours,
            -1, ( 0, 255, 0 ), 2, cv.LINE_AA )

    @functools.cached_property
    def rectancles( self ):
        for contour in self.contours:
            yield cv.boundingRect( contour )

    def crops( self ):
        for rectangle in self.rectancles:
            x, y, width, height = rectangle
            yield self.crop( x, y, width, height )
