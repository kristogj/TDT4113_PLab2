from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from random import shuffle




class Imager():

    _pixel_colors_ = {'red':(255,0,0),
                      'green': (0,255,0),
                      'blue': (0,0,255),
                      'white': (255,255,255),
                      'black': (0,0,0),
                      'pink':(255,192,203),
                      'indigo':(75,0,130),
                      'blue':(65,105,225)}


    def __init__(self,fid=False,image=False,width=100,height=100,background='black',mode='RGB'):
        self.fid = fid # The image file
        self.image = image # A PIL image object
        self.xmax = width; self.ymax = height # These can change if there's an input image or file
        self.mode = mode
        self.init_image(background=background)

    def init_image(self,background='black'):
        if self.fid: self.load_image()
        if self.image: self.get_image_dims()
        else: self.image = self.gen_plain_image(self.xmax,self.ymax,background)


################## BASICS ##################
    # Load image from file
    def load_image(self):
        self.image = Image.open(self.fid)  # the image is actually loaded as needed (automatically by PIL)
        if self.image.mode != self.mode:
            self.image = self.image.convert(self.mode)

    # Save image to a file.  Only if fid has no extension is the type argument used.  When writing to a JPEG
    # file, use the extension JPEG, not JPG, which seems to cause some problems.
    def dump_image(self,fid,type='gif'):
        fname = fid.split('.')
        type = fname[1] if len(fname) > 1 else type
        self.image.save(fname[0]+'.'+type,format=type)

    def get_image(self): return self.image
    def set_image(self,im): self.image = im

    #Åpne bilde i forhåndsvisning
    def display(self):
        self.image.show()

    def get_image_dims(self):
        self.xmax = self.image.size[0]
        self.ymax = self.image.size[1]
        return self.xmax,self.ymax

    def copy_image_dims(self,im2):
        im2.xmax = self.xmax; im2.ymax = self.ymax

    def gen_plain_image(self,x,y,color,mode=None):
        m = mode if mode else self.mode
        return Image.new(m,(x,y),self.get_color_rgb(color))

    def get_color_rgb(self,colorname): return Imager._pixel_colors_[colorname]



################## SIZE ##################
    # This returns a resized copy of the image
    def resize(self,new_width,new_height,image=False):
        image = image if image else self.image
        return Imager(image=image.resize((new_width,new_height)))

    def scale(self,xfactor,yfactor):
        return self.resize(round(xfactor*self.xmax),round(yfactor*self.ymax))

    def crop(self,box):
        img = self.image.copy().crop(box)
        return Imager(image= img)

    # Hvis bredde != høyde, så lager den resten svar slik at bredde==høyde
    def pad_to_square(self):
        img = self.image.copy()
        img_size = img.size
        longer_side = max(img_size)
        hor_padding = (longer_side - img_size[0]) / 2
        ver_padding = (longer_side - img_size[1]) / 2
        img = img.crop((
            -hor_padding,
            -ver_padding,
            img_size[0] + hor_padding,
            img_size[1] + ver_padding
        ))
        return Imager(image=img)

################## DIRECTION ##################
    _flip_ = {
        'hor': Image.FLIP_LEFT_RIGHT,
        'ver': Image.FLIP_TOP_BOTTOM
    }
    def rotate_left(self,angle,expand=True): #expand sier bare at bilde ikke skal cropes
        img = self.image.copy().rotate(angle,expand=expand)
        return Imager(image=img)

    def rotate_right(self,angle,expand=True):
        return self.rotate_left(-angle,expand)

    def flip(self,direction):
        img = self.image.copy().transpose(Imager._flip_[direction])
        return Imager(image= img)


################## MAPPING AV PIXLER ##################
    def get_pixel(self,x,y): return self.image.getpixel((x,y))
    def set_pixel(self,x,y,rgb): self.image.putpixel((x,y),rgb)

    def combine_pixels(self,p1,p2,alpha=0.5):
        return tuple([round(alpha*p1[i] + (1 - alpha)*p2[i]) for i in range(3)])

    #Gjør func med hver pixel i bilde
    #Hver pixel repr rgb(x,x,x), ved lambda x:2*x vil rgb(2x,2x,2x)
    # The use of Image.eval applies the func to each BAND, independently, if image pixels are RGB tuples.
    def map_image(self,func,image=False):
        # "Apply func to each pixel of the image, returning a new image"
        image = image if image else self.image
        return Imager(image=Image.eval(image,func)) # Eval creates a new image, so no need for me to do a copy.

    # This applies the function to each RGB TUPLE, returning a new tuple to appear in the new image.  So func
    # must return a 3-tuple if the image has RGB pixels.

    #Ser på hver pixel som en enhet, og trenger en funksjon som wta() for å gjøre noe med pixelen
    #Test med func = lamdba pixel:(100,0,0), vil bare gi et rødt bilde
    def map_image2(self,func,image=False):
        im2 = image.copy() if image else self.image.copy()
        for i in range(self.xmax):
            for j in range(self.ymax):
                im2.putpixel((i,j),func(im2.getpixel((i,j))))
        return Imager(image = im2)

    # WTA = winner take all: The dominant color becomes the ONLY color in each pixel.  However, the winner must
    # dominate by having at least thresh fraction of the total.
    def map_color_wta(self,image=False,thresh=0.34):
        image = image if image else self.image
        def wta(p):
            s = sum(p); w = max(p)
            if s > 0 and w/s >= thresh:
                return tuple([(x if x == w else 0) for x in p])
            else:
                return (0,0,0)
        return self.map_image2(wta,image)

    def map_color_removeoneRGB(self,color):
        c = {'red':0,'green':1,'blue':2}
        color = c[color]
        def roc(p):
            li = list(p)
            li[color] = 0
            return tuple(li)
        return self.map_image2(roc)


################## SCALE (ImageEnhance) ##################
    _scale_ = {"color": ImageEnhance.Color,
               "contrast": ImageEnhance.Contrast,
               "brightness": ImageEnhance.Brightness,
               "sharpness": ImageEnhance.Sharpness}

    #Demper eller forsterker scale
    def scaleX(self,scale,image=False,degree=0.5):
        image = image if image else self.image
        return Imager(image= self._scale_[scale](image).enhance(degree))

    #Gjør bilde svart/hvit
    def gen_grayscale(self,image=False): return self.scaleX("color",image=image,degree=0)

################## FILTER (ImageFilter) ##################
    _filter_ = {"gaussianblur":ImageFilter.GaussianBlur,
                "boxblur":ImageFilter.BoxBlur,
                "unsharp":ImageFilter.UnsharpMask,
                "kernel":ImageFilter.Kernel,
                "rankfilter":ImageFilter.RankFilter,
                "medianfilter":ImageFilter.MedianFilter,
                "minfilter":ImageFilter.MinFilter,
                "maxfilter":ImageFilter.MaxFilter,
                "modefilter":ImageFilter.ModeFilter}

    def xBlur(self,blur,image=False,radius=2):
        image = image if image else self.image
        f = self._filter_[blur](radius)
        return Imager(image = image.filter(f))

    def unsharp(self,image=False,radius=2,percent=150,thresold=3):
        image = image if image else self.image
        f = self._filter_["unsharp"](radius,percent,thresold)
        return Imager(image=image.filter(f))

    #Litt usikker hva denne effekten gjør nøyaktig
    def kernel(self,size,kernel,image=False,scale=250,offset=0):
        image = image if image else self.image
        f = self._filter_["kernel"](size,kernel,scale=scale,offset=offset)
        return Imager(image=image.filter(f))

    def rank(self,rank,image=False,size=3):
        image = image if image else self.image
        f = self._filter_[rank](size = size)
        return Imager(image=image.filter(f))

################## KOMBINER BILDER ##################
## The two concatenate operations will handle images of different sizes

    # Limer im2 over self.img
    def paste(self, im2, x0=0, y0=0):
        self.image.paste(im2.get_image(), (x0, y0, x0 + im2.xmax, y0 + im2.ymax))

    def frame(self,color,borde_size=7,image=False):
        image = image if image else self.image
        width,height = image.size[0]+(2*borde_size),image.size[1]+(2*borde_size)
        frame = self.gen_plain_image(width,height,color,mode="RGB")
        frame.paste(image,(borde_size,borde_size))
        return Imager(image=frame)

    #Legg to bilder ovenfor hverandre
    def concat_vert(self,im2=False,background='black'):
        im2 = im2 if im2 else self # concat with yourself if no other imager is given.
        im3 = Imager()
        im3.xmax = max(self.xmax,im2.xmax) #Finner max bredde
        im3.ymax = self.ymax + im2.ymax
        im3.image = im3.gen_plain_image(im3.xmax,im3.ymax,background)
        im3.paste(self,0,0)
        im3.paste(im2, 0,self.ymax) #paste limer bildene over img3
        return im3

    #Legg to bilder ved siden av hverandre
    def concat_horiz(self,im2=False,background='black'):
        im2 = im2 if im2 else self # concat with yourself if no other imager is given.
        im3 = Imager()
        im3.ymax = max(self.ymax,im2.ymax) #Finner maxhøyde
        im3.xmax = self.xmax + im2.xmax
        im3.image = im3.gen_plain_image(im3.xmax,im3.ymax,background)
        im3.paste(self, 0,0)
        im3.paste(im2, self.xmax,0) #paste limer bildene over img3
        return im3

    #Tar inn en liste av Imager objekter, lager collage
    #Kollonner * rader må være lik antall bilder
    #Resizer underveis
    def create_collage(self,width,height,cols,rows,listofimages):
        thumb_width = width//cols
        thumb_height = height//rows
        new_img = Image.new('RGB',(width,height))
        imgs = [self.resize(thumb_width,thumb_height)]
        for pic in listofimages:
            img = pic.resize(thumb_width,thumb_height)
            imgs.append(img)
        i,x,y = 0,0,0
        for col in range(cols):
            for row in range(rows):
                print(i,x,y)
                new_img.paste(imgs[i].image,(x,y))
                i+=1
                y+=thumb_height
            x+=thumb_width
            y=0
        return Imager(image=new_img)

    #Blander to bilder ved å legge dem over hverandre, med mindre opacity på øverste
    #Må være samme størrelse
    def morph(self,img2,alpha=0.5):
        img = Image.blend(self.image,img2.image,alpha) #Legger img2 over img med opacity alpha
        return Imager(image=img)

    def morph4(self,im2):
        im3 = self.morph(im2,alpha=0.33)
        im4 = self.morph(im2,alpha=0.66)
        return self.concat_horiz(im3).concat_vert(im4.concat_horiz(im2))

    def morphroll(self,im2,steps=3):
        delta_alpha = 1/(1+steps)
        roll = self
        for i in range(steps):
            alpha = (i + 1)*delta_alpha
            roll = roll.concat_horiz(self.morph(im2,alpha))
        roll = roll.concat_horiz(im2)
        return roll


    # Put a picture inside a picture inside a picture....
    def tunnel(self,levels=5, scale=0.75):
        if levels == 0: return self
        else:
            child = self.scale(scale,scale) # child is a scaled copy of self
            child.tunnel(levels-1,scale)
            dx = round((1-scale)*self.xmax/2); dy = round((1-scale)*self.ymax/2)
            self.paste(child, dx,dy)
            return self

    #Må være samme størrelse
    def morphtunnel(self,im2,levels=5,scale=0.75):
        return self.tunnel(levels,scale).morph4(im2.tunnel(levels,scale))


################## DRAW ##################

    #Skriver tekst øverst til venstre
    def draw_text(self,text,size=30,image=False,opacity=1):
        image = image if image else self.image
        image = image.convert("RGBA")
        txt = Image.new("RGBA",image.size,(255,255,255,0))
        fnt = ImageFont.truetype("fonts/font2.ttf",size)
        d = ImageDraw.Draw(txt)
        d.text((10, 10), text, font=fnt, fill=(0, 0, 0, int(255*opacity)))
        out = Image.alpha_composite(image,txt)
        return Imager(image=out)

    def draw_cross(self,image=False,width=10,fill="red"):
        image = image if image else self.image
        fill = self._pixel_colors_[fill]
        draw = ImageDraw.Draw(image)
        draw.line((0, 0) + image.size, fill=fill,width=width)
        draw.line((0, image.size[1], image.size[0], 0), fill=fill,width=width)
        del draw
        return Imager(image = image)


################## OPS ('Ready-made' image processing operations ##################

    #cutoff - prosent to cut of histogram
    #ignore - background pixel value (None for no background)
    def autocontrast(self,image=False,cutoff=0,ignore=False):
        image = image if image else self.image
        image = ImageOps.autocontrast(image,cutoff=cutoff,ignore=ignore)
        return Imager(image=image)

    def grayscaleOPS(self,image=False):
        image = image if image else self.image
        image = ImageOps.grayscale(image)
        return Imager(image=image)

    #Fargelegg svart/hvit bilde
    def colorize(self,black,white,image=False):
        image = image if image else self.image
        black = Imager._pixel_colors_[black]
        white = Imager._pixel_colors_[white]
        image = ImageOps.colorize(image,black,white)
        return Imager(image=image)

    #Fjerner x pixler fra hver side
    def cropOPS(self,pixels,image=False):
        image = image if image else self.image
        image = ImageOps.crop(image,border=pixels)
        return Imager(image=image)

    #Equalize the image histogram. This function applies a non-linear mapping to the input image, in order
    #to create a uniform distribution of grayscale values in the output image.
    #Va litt fet..
    def equalize(self,image=False,mask=None):
        image = image if image else self.image
        image = ImageOps.equalize(image,mask=mask)
        return Imager(image=image)

    #Gir bildets negativ
    def invert(self,image=False):
        image = image if image else self.image
        image = ImageOps.invert(image)
        return Imager(image=image)

    # Threshold = 255 ingen endring
    # Threshold = 0 samme som invert
    # Inverterer altså alle piksler over threshold
    def solarize(self, threshold=128, image=False):
        image = image if image else self.image
        image = ImageOps.solarize(image, threshold=threshold)
        return Imager(image=image)

    #Reduser antall bit for hver farge kanal
    #Bits (1-8)
    def posterize(self,bits=2,image=False):
        image = image if image else self.image
        if bits>8:bits=8
        image = ImageOps.posterize(image,bits)
        return Imager(image=image)


################## My Ideas ##################

    def shuffleImageRows(self,image=False,faktor=100):
        image = image if image else self.image
        liste = list(image.getdata())
        rows = []
        for x in range(0,len(liste),faktor*image.size[0]):
            rows.append(liste[x:x+faktor*image.size[0]])
        shuffle(rows)
        res = []
        for row in rows:
            for tup in row:
                res.append(tup)
        im2 = Image.new(image.mode,image.size)
        im2.putdata(res)
        return Imager(image=im2)

    def shuffleImageCol(self,image=False,faktor=100):
        image = image if image else self.image
        image = Imager(image=image)
        image = image.rotate_left(90)
        image = image.shuffleImageRows(faktor=faktor)
        image = image.rotate_right(90)
        return image







### *********** TESTS ************************

# Note: the default file paths for these examples are for unix!

#Fjerner en farge fra bildene, setter dem sammen horizontalt
def remove_RGB_3imgconcat(imagepath="images/brain.jpeg"):
    img1 = Imager(imagepath)
    noRed = img1.map_color_removeoneRGB("red")
    noGreen = img1.map_color_removeoneRGB("green")
    noBlue = img1.map_color_removeoneRGB("blue")
    onetwo = noRed.concat_horiz(noGreen)
    all = onetwo.concat_horiz(noBlue)
    return all

def ptest1(fid1='images/kdfinger.jpeg', fid2="images/einstein.jpeg",steps=5,newsize=250):
    im1 = Imager(fid1); im2 = Imager(fid2)
    im1 = im1.resize(newsize,newsize); im2 = im2.resize(newsize,newsize)
    roll = im1.morphroll(im2,steps=steps)
    roll.display()
    return roll

def ptest2(fid1='images/einstein.jpeg',outfid='images/tunnel.jpeg',levels=3,newsize=250,scale=0.8):
    im1 = Imager(fid1);
    im1 = im1.resize(newsize,newsize);
    im2 = im1.tunnel(levels=levels,scale=scale)
    im2.display()
    im2.dump_image(outfid)
    return im2

def ptest3(fid1='images/kdfinger.jpeg', fid2="images/einstein.jpeg",newsize=250,levels=4,scale=0.75):
    im1 = Imager(fid1); im2 = Imager(fid2)
    im1 = im1.resize(newsize,newsize); im2 = im2.resize(newsize,newsize)
    box = im1.mortun(im2,levels=levels,scale=scale)
    box.display()
    return box

def reformat(in_fid, out_ext='jpeg',scalex=1.0,scaley=1.0):
    base, extension = in_fid.split('.')
    im = Imager(in_fid)
    im = im.scale(scalex,scaley)
    im.dump_image(base,out_ext)

