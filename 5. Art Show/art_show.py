from imager2 import Imager
import imager2
#Skriver all kode i imager2
#bruker denne filen for å redigere og vise bilder
#artshow


img1 = Imager("images/meg.jpeg")
img2 = Imager("images/robot.jpeg")
img3 = Imager("images/einstein.jpeg")
img4 = Imager("images/fibonacci.jpeg")
img5 = Imager("images/fisheggs.jpeg")
img6 = Imager("images/kdfinger.jpeg")
list = [img2,img3,img4,img5,img6]

im1 = "images/fibonacci.jpeg"
im2 = "images/kdfinger.gif"
im3 = "images/brain.jpeg"
imager2.artistic(im1,im2,im3).display()

