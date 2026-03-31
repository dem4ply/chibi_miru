import functools
import io
import logging

import cv2 as cv
from PIL.Image import Image as PIL_image
from chibi.file import Chibi_path
from chibi.madness.string import generate_b64_unsecure

from .snippets import pil_to_cv
from chibi_miru.barcode import Barcode
from chibi_miru.draw import Draw


logger = logging.getLogger( 'chibi.miru.image' )


class Image:
    def __init__( self, ndarray, name=None, is_gray=False, *, origin=None ):
        # is a path
        if isinstance( ndarray, str ):
            path = Chibi_path( ndarray )
            self._path = path
            self.name = self.path.base_name
            ndarray = cv.imread( path, cv.IMREAD_COLOR )
        elif isinstance( ndarray, PIL_image ):
            if name is None:
                self.name = ndarray.filename or generate_b64_unsecure()
            ndarray = pil_to_cv( ndarray )
        else:
            self.name = name

        if origin is not None:
            self.origin = origin
            origin_name = Chibi_path( self.origin.name )
            self.name = (
                f"{origin_name.file_name}__{self.name}"
                f"{origin_name.extension}"
            )
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
        cv.waitKey( 1 )  # se nesesita para ver la imagen

    def save( self, path ):
        if isinstance( path, io.BytesIO ):
            file_name = Chibi_path( self.name )
            success, buff = cv.imencode( f".{file_name.extension}", self.raw )
            path.write( buff )
            path.seek( 0 )
        elif isinstance( path, str ):
            cv.imwrite( path + self.name, self.raw )
        else:
            raise NotImplementedError(
                'no imprementado este metodo de guardado {str(type(path))} '
                '{str(path)}'
            )

    @property
    def path( self ):
        return self._path

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
        return Resize(
            result, origin=self, dimensions=dimensions,
            is_gray=self.is_gray )

    def crop( self, x, y, width, height ):
        crop_raw = self.raw[ y:y + height, x:x + width ]
        return Image(
            crop_raw, name=f'crop_{x}_{y}_{width}_{height}', origin=self,
            is_gray=self.is_gray )

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
            gray, name="gray", is_gray=True, origin=self )

    def close( self ):
        if hasattr( self, '_windows_name' ):
            cv.destroyWindow( self._windows_name )
            cv.waitKey( 1 )  # se nesesita, no se porque
            logger.debug( f"cerro la ventana {self._windows_name}" )

    def close_all( self ):
        cv.destroyAllWindows()
        logger.debug( "cerrando todas las ventanas" )

    def wait( self, t ):
        cv.waitKey( t )


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


class Processing():
    def __init__( self, *args, parent, **kw ):
        self.parent = parent

    def binary( self, a=150, b=255 ):
        threshold_value, thresh = cv.threshold(
            self.parent.gray.raw, a, b, cv.THRESH_BINARY )
        return Binary(
            thresh, origin=self.parent, threshold_value=threshold_value,
            a=a, b=b )

    def dilate( self, kernel, iterations=1 ):
        """
        Examples
        --------
        >>>kernel = np.ones((5, 5), np.uint8)
        """
        dilated_value = cv.dilate( self.parent.raw, kernel, iterations=1 )
        return Dilate( dilated_value, origin=self.parent, kernel=kernel, )

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

    def _ocr_contours( self ):
        thresh = self.parent.processing.otsu()
        rect_kernel = cv.getStructuringElement( cv.MORPH_RECT, ( 18, 18 ) )
        dilation = thresh.processing.dilate( rect_kernel )
        contours, hierarchy = cv.findContours(
            image=dilation.raw, mode=cv.RETR_EXTERNAL,
            method=cv.CHAIN_APPROX_NONE )

        return Contours(
            self.parent.raw.copy(), origin=self.parent,
            contours=contours, hierarchy=hierarchy )

    @functools.cached_property
    def ocr( self ):
        return OCR( self, parent=self.parent )


class OCR:
    def __init__( self, *args, parent, **kw ):
        self.parent = parent

    def to_string( self ):
        import pytesseract
        result = pytesseract.image_to_string( self.parent.raw, )
        return result
