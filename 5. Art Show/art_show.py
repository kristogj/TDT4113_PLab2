from imager2 import Imager
from PIL import Image
from PIL import ImageColor



class KGImager(Imager):

    _flip_ = {
        'hor':Image.FLIP_LEFT_RIGHT,
        'ver':Image.FLIP_TOP_BOTTOM
    }

#CHANGE DIRECTION
    #Roterer bilde. expand bestemmer om bilde skal beholde dimensjonen eller ikke
    #Blir cropet ved rotasjon hvis False
    def rotate_left(self,angle,expand=True):
        img = self.image.copy().rotate(angle,expand=expand)
        return KGImager(image=img)

    def rotate_right(self,angle,expand=True):
        self.rotate_left(-angle,expand)

    def flip(self,direction):
        img = self.image.copy()
        img = img.transpose(KGImager._flip_[direction])
        return KGImager(image= img)

#CROP
    def crop(self,box):
        return self.image.crop(box)

    #Hvis bredde != høyde, så lager den resten svar slik at bredde==høyde
    def pad_to_square(self):
        img_size = self.image.size
        longer_side = max(img_size)
        hor_padding = (longer_side - img_size[0]) / 2
        ver_padding = (longer_side - img_size[1]) / 2
        self.image = self.image.crop((
            -hor_padding,
            -ver_padding,
            img_size[0] + hor_padding,
            img_size[1] + ver_padding
        ))


        

obj = KGImager("images/campus.jpeg")
obj.rotate_left(90).display()

















