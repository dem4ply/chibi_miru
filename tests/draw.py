from unittest import TestCase
from chibi_miru.draw import to_bgr
from tests.image import Test_image


class Test_draw( TestCase ):
    def test_transform_rgb_to_bgr_tuple( self ):
        self.assertEqual( ( 255, 0, 0 ), to_bgr( ( 0, 0, 255 ) ) )
        self.assertEqual( ( 0, 255, 0 ), to_bgr( ( 0, 255, 0 ) ) )
        self.assertEqual( ( 0, 0, 255 ), to_bgr( ( 255, 0, 0 ) ) )

    def test_transform_rgb_to_bgr_list( self ):
        self.assertEqual( [ 255, 0, 0 ], to_bgr( [ 0, 0, 255 ] ) )
        self.assertEqual( [ 0, 255, 0 ], to_bgr( [ 0, 255, 0 ] ) )
        self.assertEqual( [ 0, 0, 255 ], to_bgr( [ 255, 0, 0 ] ) )


class Test_draw_text( Test_image ):
    def test_can_put_text_in_image( self ):
        self.image.draw.text( "hello my little world!!!", ( 10, 10 ) )
        self.image.show()
        """
        k = ""
        while True:
            k = self.image.wait( 10 )
            if k > 0:
                print( k )
            if k == 27:
                break
        """
