from chibi.snippet.string import decode


class QR:
    def __init__( self, barcode ):
        if barcode.type != "QRCODE":
            raise NotImplementedError

        self.data = barcode.data
        self.rectagle = (
            ( barcode.rect.left, barcode.rect.top ),
            barcode.rect.width, barcode.rect.height, )

    def __str__( self ):
        return decode( self.data )
