import cv2 as cv
import logging
from chibi_miru.image import Image

logger = logging.getLogger( 'chibi.miru.cam' )


class Chibi_cam:
    def __init__( self, cam_number=0, name=None ):
        self.cam_number = cam_number
        self._cam = cv.VideoCapture( self.cam_number )
        if name is None:
            self.name = "cam {}".format( cam_number )

    @property
    def is_open( self ):
        return self._cam.isOpened()

    @property
    def read( self ):
        return Image( self.raw_read, name=self.name )

    @property
    def raw_read( self ):
        is_read, image = self._cam.read()
        if not is_read:
            logger.error(
                f"no pudo optner la imagen de la camara {self.cam_number}" )
        return image

    def __del__( self ):
        self._cam.release()
        logger.debug( f"camara {self.cam_number} liberada" )
