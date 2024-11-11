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
            
        print(img_array)
        rows, cols = img_array.shape
        result = []
        
        for d in range(rows + cols - 1):
            if d % 2 == 0:
                # Traverse from top to bottom-left (bottom-right if within bounds)
                r = min(d, rows - 1)
                c = max(0, d - r)
                while r >= 0 and c < cols:
                    result.append(int(img_array[r, c]))
                    r -= 1
                    c += 1
            else:
                # Traverse from left to top-right (bottom-left if within bounds)
                c = min(d, cols - 1)
                r = max(0, d - c)
                while c >= 0 and r < rows:
                    result.append(int(img_array[r, c]))
                    c -= 1
                    r += 1

        print(result)