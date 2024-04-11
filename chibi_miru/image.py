import cv2 as cv
import logging
import numpy as np
import functools
from chibi_miru.draw import Draw
from chibi.madness.string import generate_b64_unsecure
from chibi_miru.barcode import Barcode
from PIL.Image import Image as PIL_image
from .snippets import pil_to_cv

logger = logging.getLogger( 'chibi.miru.image' )


class Image:
    def __init__( self, ndarray, name=None, is_gray=False, *, origin=None ):
        if isinstance( ndarray, str ):
            self.name = ndarray
            ndarray = cv.imread( ndarray, cv.IMREAD_COLOR )
        elif isinstance( ndarray, PIL_image ):
            if name is None:
                self.name = ndarray.filename or generate_b64_unsecure()
            ndarray = pil_to_cv( ndarray )
        else:
            self.name = name

        if origin is not None:
            self.origin = origin
            self.name = f"{self.origin.name}__{self.name}"
            self.is_gray = self.origin.is_gray

        self.is_gray = is_gray
        self.raw = ndarray

    def show( self, name=None, img=None ):
        if img is None:
            img = self.raw
        if name is None:
            name = self.name
        self._windows_name = name
        cv.imshow( name, img )
        cv.waitKey( 1 ) # se nesesita para ver la imagen

    @functools.cached_property
    def dimentions( self ):
        h, w = self.raw.shape[ :2 ]
        return w, h

    @functools.cached_property
    def ratio( self ):
        w, h = self.dimentions
        return w / h

    def resize( self, width=None, height=None, interpolation=cv.INTER_AREA ):
        dimensions = None
        w, h = self.dimentions

        if width is None and height is None:
            return self
        if width is None:
            r = height / float( h )
            dimensions = ( int( w * r ), height )
        else:
            r = width / float( w )
            dimensions = ( width, int( h * r ) )

        result = cv.resize( self.raw, dimensions, interpolation=interpolation )
        return Processed( result, origin=self, is_gray=self.is_gray )

    @functools.cached_property
    def barcode( self ):
        return Barcode( self.gray.raw )

    @functools.cached_property
    def draw( self ):
        return Draw( self.raw )

    @functools.cached_property
    def processing( self ):
        return Processing( parent=self )

    @functools.cached_property
    def detect( self ):
        return Detect( parent=self )

    @functools.cached_property
    def gray( self ):
        if self.is_gray:
            return self
        gray = cv.cvtColor( self.raw, cv.COLOR_BGR2GRAY )
        return type( self )(
            gray, name=f"{self.name}__gray", is_gray=True, origin=self )

    def close( self ):
        if hasattr( self, '_windows_name' ):
            cv.destroyWindow( self._windows_name )
            cv.waitKey( 1 ) # se nesesita, no se porque
            logger.debug( f"cerro la ventana {self._windows_name}" )

    def close_all( self ):
        cv.destroyAllWindows()
        logger.debug( f"cerrando todas las ventanas" )

    def wait( self, t ):
        cv.waitKey( t )


class Processed( Image ):
    def __init__( self, *args, origin, **kw ):
        super().__init__( *args, origin=origin, **kw )


class Threshold( Processed ):
    def __init__( self, *args, threshold_value, **kw ):
        super().__init__( *args, **kw )
        self.threshold_value = threshold_value


class Contours( Processed ):
    def __init__( self, *args, contours, hierarchy, **kw ):
        super().__init__( *args, **kw )
        self.contours = contours
        self.hierarchy = hierarchy
        cv.drawContours(
            self.raw, contours,
            -1, ( 0, 255, 0 ), 2, cv.LINE_AA )


class Processing():
    def __init__( self, *args, parent, **kw ):
        self.parent = parent

    def binary( self, a=150, b=255 ):
        threshold_value, thresh = cv.threshold(
            self.parent.gray.raw, a, b, cv.THRESH_BINARY )
        return Threshold(
            thresh, origin=self.parent, threshold_value=threshold_value )

    def dilate( self, threshold_value, kernel, iterations=1 ):
        """
        Examples
        --------
        >>>kernel = np.ones((5, 5), np.uint8)
        """
        dilated_value = cv.dilate( threshold_value, kernel, iterations=1 )
        return Dilate( dilated_value, origin=self.parent,  )

    def gaussian_blur( self, x=5, y=5, kernel=0 ):
        """
        aplica desenfoque gausiano

        Parameters
        ----------
        x: int
        y: int
        kernel: int

        Examples
        ========
        >>>gaussian_blur
        """
        blur = cv.GaussianBlur( self.parent.gray.raw, ( x, y ), kernel )
        return Processed(
            blur, origin=self.parent.gray, name="gaussian_blur" )

    def otsu( self, a=0, b=255 ):
        threshold_value, thresh = cv.threshold(
            self.parent.gray.raw, a, b, cv.THRESH_OTSU )
        return Threshold(
            thresh, origin=self.parent, threshold_value=threshold_value )


class Detect:
    def __init__( self, *args, parent, **kw ):
        self.parent = parent

    def contours( self ):
        thresh = self.parent.processing.otsu()
        contours, hierarchy = cv.findContours(
            image=thresh.raw, mode=cv.RETR_TREE,
            method=cv.CHAIN_APPROX_NONE )
        return Contours(
            self.parent.raw.copy(), origin=self.parent,
            contours=contours, hierarchy=hierarchy )
