from imager2 import Imager
#Skriver all kode i imager2
#bruker denne filen for å redigere og vise bilder
#artshow


img1 = Imager("images/campus.jpeg")
img2 = Imager("images/robot.jpeg")
img3 = Imager("images/einstein.jpeg")
img4 = Imager("images/fibonacci.jpeg")
img5 = Imager("images/fisheggs.jpeg")
img6 = Imager("images/kdfinger.jpeg")
list = [img2,img3,img4,img5,img6]


img1.create_collage(500,500,3,2,list).display()




















