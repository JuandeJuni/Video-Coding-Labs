from PIL import Image
import subprocess
import numpy as np
import pywt
import matplotlib.pyplot as plt
from scipy.fftpack import dctn, idctn
class VideoEncoder:
    
    #task 2
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
    
    #task 3
    def resizeImage(filename, width, height,compression):
        command = "ffmpeg -i inputs/"+filename+" -vf scale="+str(width)+":"+str(height)+" -qscale:v "+str(compression)+" -y"+" outputs/resized"+filename
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #task 4
    def serpentine(filename):        
        with Image.open(f"inputs/{filename}") as img:
            grayscale = img.convert('L')
            img_array = np.array(grayscale, dtype=np.uint8)
            
        print(img_array)
        rows, cols = img_array.shape
        result = []
        
        for d in range(rows + cols - 1):
            if d % 2 == 0:
                
                r = min(d, rows - 1)
                c = max(0, d - r)
                while r >= 0 and c < cols:
                    result.append(int(img_array[r, c]))
                    r -= 1
                    c += 1
            else:
                
                c = min(d, cols - 1)
                r = max(0, d - c)
                while c >= 0 and r < rows:
                    result.append(int(img_array[r, c]))
                    c -= 1
                    r += 1

        print("Result:",result)
        
    #task 5.1 + comment the results
    def color_to_bw(filename, compression):
        command = f"ffmpeg -i inputs/{filename} -vf format=gray -q:v {compression} -y outputs/bw{filename}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    #task 5.2
    def runlength_encode(bytes_array):
        result = ""
        count = 1
        for i in range(1, len(bytes_array)):
            if bytes_array[i] == bytes_array[i - 1]:
                count += 1
            else:
                result+=f"{bytes_array[i - 1]}{count}"
                count = 1
        result+=f"{bytes_array[i - 1]}{count}"
        return result.encode('utf-8')
    
#task 6
class DCT:
    def convert(filename): 
        with Image.open(f"inputs/{filename}") as img:
            grayscale = img.convert('L')
            img_array = np.array(grayscale, dtype=np.uint8)
        dct_image = dctn(img_array, norm = 'ortho')
        return dct_image

    def decoder(dct_image):
        estimated_image = idctn(dct_image, norm = 'ortho')
        plt.imshow(estimated_image, cmap = 'gray')
        plt.title('Estimated image (DCT)')
        plt.show()
#task 7            
class DWT:
    def convert(filename):
        with Image.open(f"inputs/{filename}") as img:
            grayscale = img.convert('L')
            img_array = np.array(grayscale, dtype=np.uint8)
        coeffs = pywt.dwt2(img_array, 'haar')
        LL,(LH,HL,HH) = coeffs
        fig, ax = plt.subplots(1, 4, figsize=(12, 12))
        subbands = [LL, LH, HL, HH]
        subbands_string = ['LL (Smooth parts of the image)', 'LH (Horizontal details)', 'HL (Vertical details)', 'HH (Diagonal details)']
        for i,s in enumerate(subbands):
            ax[i].imshow(s, cmap='gray')
            ax[i].set_title(subbands_string[i])
            ax[i].axis('off')
        plt.show()
        return subbands
    def decode(LL, LH, HL, HH):
        estimated_image = pywt.idwt2((LL, (LH, HL, HH)), 'haar')
        plt.imshow(estimated_image, cmap = 'gray')
        plt.title('Estimated image (DWT)')
        plt.show()
        return estimated_image
            
            


