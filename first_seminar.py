import ffmpeg
from PIL import Image
import numpy as np
class VideoEncoder:
    def RGBtoYUV(r,g,b):
        y = round(0.257*r + 0.504*g + 0.098*b+16)
        u = round(-0.148*r - 0.291*g + 0.439*b+128)
        v = round(0.439*r - 0.368*g - 0.071*b+128)
        return y,u,v
    
        
    def YUVtoRGB(y,u,v):
        r = round(1.164*(y-16) + 1.596*(v-128))
        g = round(1.164*(y-16) - 0.813*(v-128) - 0.391*(u-128))
        b = round(1.164*(y-16) + 2.018*(u-128))
        return r,g,b
    
    def resizeImage(filepath, width, height,compression):
        resized = ffmpeg.input(filepath).filter("scale", width, height)
        ffmpeg.output(resized,"resized"+filepath, q=compression).run()
    def serpentine(filepath):
        with Image.open(filepath) as img:
            grayscale = img.convert('L')
            img_array = np.array(grayscale, dtype=np.uint8)
        col = 0
        row = 0
        while (col != img_array.shape[1] and row != img_array.shape[0]):
            if col == 0:
                row += 1

        

        print(img_array)
        # print(position)



