import functools
import logging

import cv2 as cv
from chibi.file import Chibi_path


class Detect:
    def __init__( self, *args, parent, **kw ):
        self.parent = parent

    def contours( self ):
        thresh = self.parent.processing.otsu()
        contours, hierarchy = cv.findContours(
            image=thresh.raw, mode=cv.RETR_TREE,
            method=cv.CHAIN_APPROX_NONE )
        from chibi_miru.processed import Contours
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

        from chibi_miru.processed import Contours
        return Contours(
            self.parent.raw.copy(), origin=self.parent,
            contours=contours, hierarchy=hierarchy )

    @functools.cached_property
    def ocr( self ):
        return OCR( self, parent=self.parent )

    @functools.cached_property
    def cascade( self ):
        return Cascade( parent=self.parent )


class OCR:
    def __init__( self, *args, parent, **kw ):
        self.parent = parent

    def to_string( self ):
        import pytesseract
        result = pytesseract.image_to_string( self.parent.raw, )
        return result


class Cascade:
    def __init__( self, *args, parent, **kw ):
        self.parent = parent

    @property
    def models( self ):
        return Cascade_models()

    def classifier( self, model ):
        return cv.CascadeClassifier( model )

    @property
    def haarcascade_eye( self ):
        classifier = self.classifier( self.models.haarcascade_eye )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_frontalcatface_extended( self ):
        classifier = self.classifier(
            self.models.haarcascade_frontalcatface_extended )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_righteye_2splits( self ):
        classifier = self.classifier(
            self.models.haarcascade_righteye_2splits )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_upperbody( self ):
        classifier = self.classifier(
            self.models.haarcascade_upperbody )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_profileface( self ):
        classifier = self.classifier(
            self.models.haarcascade_profileface )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_russian_plate_number( self ):
        classifier = self.classifier(
            self.models.haarcascade_russian_plate_number )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_lefteye_2splits( self ):
        classifier = self.classifier(
            self.models.haarcascade_lefteye_2splits )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_frontalface_alt_tree( self ):
        classifier = self.classifier(
            self.models.haarcascade_frontalface_alt_tree )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_eye_tree_eyeglasses( self ):
        classifier = self.classifier(
            self.models.haarcascade_eye_tree_eyeglasses )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_frontalface_alt2( self ):
        classifier = self.classifier(
            self.models.haarcascade_frontalface_alt2 )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_frontalface_alt( self ):
        classifier = self.classifier(
            self.models.haarcascade_frontalface_alt )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_license_plate_rus_16stages( self ):
        classifier = self.classifier(
            self.models.haarcascade_license_plate_rus_16stages )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_smile( self ):
        classifier = self.classifier(
            self.models.haarcascade_smile )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_frontalcatface( self ):
        classifier = self.classifier(
            self.models.haarcascade_frontalcatface )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_fullbody( self ):
        classifier = self.classifier(
            self.models.haarcascade_fullbody )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_lowerbody( self ):
        classifier = self.classifier(
            self.models.haarcascade_lowerbody )
        results = classifier.detectMultiScale( self.parent.raw )
        return results

    @property
    def haarcascade_frontalface_default( self ):
        classifier = self.classifier(
            self.models.haarcascade_frontalface_default )
        results = classifier.detectMultiScale( self.parent.raw )
        return results


class Cascade_models:
    @property
    def base_folder( self ):
        return Chibi_path( cv.data.haarcascades )

    @property
    def haarcascade_eye( self ):
        return self.base_folder + 'haarcascade_eye.xml'

    @property
    def haarcascade_frontalcatface_extended( self ):
        return self.base_folder + 'haarcascade_frontalcatface_extended.xml'

    @property
    def haarcascade_righteye_2splits( self ):
        return self.base_folder + 'haarcascade_righteye_2splits.xml'

    @property
    def haarcascade_upperbody( self ):
        return self.base_folder + 'haarcascade_upperbody.xml'

    @property
    def haarcascade_profileface( self ):
        return self.base_folder + 'haarcascade_profileface.xml'

    @property
    def haarcascade_russian_plate_number( self ):
        return self.base_folder + 'haarcascade_russian_plate_number.xml'

    @property
    def haarcascade_lefteye_2splits( self ):
        return self.base_folder + 'haarcascade_lefteye_2splits.xml'

    @property
    def haarcascade_frontalface_alt_tree( self ):
        return self.base_folder + 'haarcascade_frontalface_alt_tree.xml'

    @property
    def haarcascade_eye_tree_eyeglasses( self ):
        return self.base_folder + 'haarcascade_eye_tree_eyeglasses.xml'

    @property
    def haarcascade_frontalface_alt2( self ):
        return self.base_folder + 'haarcascade_frontalface_alt2.xml'

    @property
    def haarcascade_frontalface_alt( self ):
        return self.base_folder + 'haarcascade_frontalface_alt.xml'

    @property
    def haarcascade_license_plate_rus_16stages( self ):
        return self.base_folder + 'haarcascade_license_plate_rus_16stages.xml'

    @property
    def haarcascade_smile( self ):
        return self.base_folder + 'haarcascade_smile.xml'

    @property
    def haarcascade_frontalcatface( self ):
        return self.base_folder + 'haarcascade_frontalcatface.xml'

    @property
    def haarcascade_fullbody( self ):
        return self.base_folder + 'haarcascade_fullbody.xml'

    @property
    def haarcascade_lowerbody( self ):
        return self.base_folder + 'haarcascade_lowerbody.xml'

    @property
    def haarcascade_frontalface_default( self ):
        return self.base_folder + 'haarcascade_frontalface_default.xml'
