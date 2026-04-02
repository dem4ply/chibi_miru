import cv2 as cv
from chibi_miru.barcode import types


def to_bgr( color ):
    return color[::-1]


class Draw:
    def __init__( self, image ):
        self.image = image

    def line( self, start, end, color, size=1 ):
        cv.line( self.image, start, end, to_bgr( color ), size )

    def rectangle( self, start, w, h, color, size=1 ):
        cv.rectangle(
            self.image, start, ( start[0] + w, start[1] + h ),
            to_bgr( color ), size )

    def barcode_boundary( self, barcode, color, size=1 ):
        if isinstance( barcode, types.QR ):
            self.rectangle(
                barcode.rectagle[0], barcode.rectagle[1],
                barcode.rectagle[2], color, size  )
        else:
            raise NotImplementedError

    def text( self, text, position ):
        """
        pone texto en la imagen

        Arguments
        ---------
        text: string
        position: Vector2 or tuple of 2 ints
        """
        font = cv.FONT_HERSHEY_SIMPLEX
        ( width, height ), baseline = cv.getTextSize(
            text, font, 1, 1 )
        x, y = position
        if y - height < 0:
            y = y + height
        position = ( x, y )
        cv.putText(
            self.image, text,
            position, font, 1, ( 0, 255, 0 ), 1,
            cv.LINE_AA )
