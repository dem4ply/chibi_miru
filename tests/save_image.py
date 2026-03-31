from chibi.file.temp import Chibi_temp_path
from tests.image import Test_image


class Test_save_images( Test_image ):
    def setUp( self ):
        super().setUp()
        self.path = Chibi_temp_path()
        self.assert_count_files( 0 )

    def assert_count_files( self, amount ):
        count = len( list( self.path.ls() ) )
        self.assertEqual( count, amount )

    def get_single( self ):
        images = list( self.path.ls() )
        self.assertEqual( len( images ), 1 )
        return images[0]

    def test_save_should_create_a_file_with_the_name( self ):
        self.image.save( self.path )
        path = self.path + self.image.name
        self.assertTrue( path.exists )

    def test_save_image_and_resize( self ):
        resize = self.image.resize( width=100 )
        self.image.save( self.path )
        resize.save( self.path )
        self.assert_count_files( 2 )

    def test_save_resize_should_have_resize_name( self ):
        resize = self.image.resize( width=100 )
        resize.save( self.path )
        self.assert_count_files( 1 )
        new_image = self.get_single()
        self.assertIn( "resize_100x", new_image.base_name )
        self.assertNotIn( "none", new_image.base_name.lower() )

    def test_binary_should_have_expected_name( self ):
        binary = self.image.processing.binary()
        binary.save( self.path )
        new_image = self.get_single()
        self.assertIn( "binary_", new_image.base_name )
        self.assertNotIn( "none", new_image.base_name.lower() )

    def test_binary_with_args_should_have_expected_name( self ):
        binary = self.image.processing.binary( 127, 255 )
        binary.save( self.path )
        new_image = self.get_single()
        self.assertIn( "binary_127_255", new_image.base_name )
        self.assertNotIn( "none", new_image.base_name.lower() )

    def test_gray_should_have_gray_in_name( self ):
        image = self.image.gray
        image .save( self.path )
        new_image = self.get_single()
        self.assertIn( "gray", new_image.base_name )
        self.assertNotIn( "none", new_image.base_name.lower() )

    def test_3_images_save_should_work( self ):
        self.image.save( self.path )
        self.image.gray.save( self.path )
        self.image.processing.binary().save( self.path )
        self.assert_count_files( 3 )
