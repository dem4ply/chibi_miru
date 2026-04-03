from unittest import TestCase

from tests.image import Test_image
from chibi_miru.cam import Chibi_cam


class Test_detect( Test_image ):
    def test_read_from_camerata_and_use_haarcascade_eye( self ):
        cam = Chibi_cam()
        for i in range( 100 ):
            image = cam.read
            results = image.detect.cascade.haarcascade_eye
            for x, y, w, h in results:
                image.draw.rectangle( (x, y ), w, h, ( 200, 200, 0 ) )

            image.show()
