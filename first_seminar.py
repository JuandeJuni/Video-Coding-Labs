from PIL import Image
import subprocess
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
        command = "ffmpeg -i "+filepath+" -vf scale="+str(width)+":"+str(height)+" -qscale:v "+str(compression)+" -y"+" resized"+filepath
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def serpentine(filepath):        
        with Image.open(filepath) as img:
            grayscale = img.convert('L')
            img_array = np.array(grayscale, dtype=np.uint8)
        rows = img_array.shape[0]
        cols = img_array.shape[1]
        for i in range(rows):
            
            
                
           

        

        print(img_array)



