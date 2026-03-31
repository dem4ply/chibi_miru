from pyzbar import pyzbar
from .types import QR


class Barcode:
    def __init__( self, image ):
        self.image = image

    @property
    def barcodes( self ):
        try:
            return self._barcode
        except AttributeError:
            self.scan()
            return self._barcode

    def scan( self ):
        raw = pyzbar.decode( self.image )
        result = []
        for barcode in raw:
            if ( barcode.type == "QRCODE" ):
                result.append( QR( barcode ) )
            else:
                raise NotImplementedError( str( barcode ) )
        self._barcode = result
