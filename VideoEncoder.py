from PIL import Image
import subprocess
import numpy as np
import pywt
import json
import os
import shutil
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
    def resizeImage(self,filename, width, height,compression):
        command = "ffmpeg -i inputs/"+filename+" -vf scale="+str(width)+":"+str(height)+" -qscale:v "+str(compression)+" -y"+" outputs/resized"+str(width)+"x"+str(height)+filename
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
        return result
    
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
        return result.encode('ascii')
    
    def chromaSubsampling(filename,chroma_subsampling):
        command = f"ffmpeg -i inputs/{filename} -vf format={chroma_subsampling} -y outputs/{chroma_subsampling}{filename}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def getInfo(filename):
        command = f"ffprobe -v quiet -print_format json -show_format -show_streams inputs/{filename}"
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        videoInfo = json.loads(result.stdout)
        return videoInfo
    def cutVideo(filename, start, duration):
        command = f"ffmpeg -i inputs/{filename} -ss {start} -t {duration} -c copy -y outputs/cut{filename}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def getMonoAAC(filename):
        command = f"ffmpeg -i outputs/{filename} -c:a aac -ac 1 -y outputs/mono{filename[:-4]}.aac"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def getMP3Stereo(filename,bitrate):
        command = f"ffmpeg -i outputs/{filename} -c:a libmp3lame -b:a {bitrate} -y outputs/stereo{filename[:-4]}.mp3"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def getAC3(filename):
        command = f"ffmpeg -i outputs/{filename} -c:a ac3 -y outputs/ac3{filename[:-4]}.ac3"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def packageMP4(videofilename,aacfilename,mp3filename,ac3filename):
        command = f"ffmpeg -i outputs/{videofilename} -i outputs/{aacfilename} -i outputs/{mp3filename} -i outputs/{ac3filename} -map 0:v -map 1:a -map 2:a -map 3:a -c:a copy -c:v copy -write_tmcd 0 -y outputs/packaged{videofilename[:-4]}.mp4"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def getMotion(filename):
        command = f"ffmpeg -flags2 +export_mvs -i inputs/{filename} -vf codecview=mv=pf+bf+bb -y outputs/motion{filename[:-4]}.mp4"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def getHistogram(filename):
        command = f'ffmpeg -i inputs/{filename} -vf "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay" -y outputs/histogram{filename}'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def convertToVP8(self,filename):
        command = f"ffmpeg -i inputs/{filename} -c:v libvpx -b:v 1M -c:a libvorbis -y outputs/vp8{filename[:-4]}.webm"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def convertToVP9(self,filename):
        command = f"ffmpeg -i inputs/{filename} -c:v libvpx-vp9 -b:v 2M -y outputs/vp9{filename[:-4]}.webm"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def convertToH265(self,filename):
        command = f"ffmpeg -i inputs/{filename} -c:v libx265 -b:v 1M -y outputs/h265{filename}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    def convertToAV1(self,filename):
        command = f"ffmpeg -i inputs/{filename} -c:v libaom-av1 -b:v 1M -y outputs/av1{filename[:-4]}.mkv"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def EncodingLadder(self,filename,codec):
        resolutions = ["2560x1440","1920x1080","1280x720","854x480","640x360","426x240"]
        codecs = ["vp8","vp9","h265","av1"]
        if codec not in codecs:
            return False
        os.makedirs("outputs/ladder", exist_ok=True)

        for res in resolutions:
            width,height = res.split("x")
            self.resizeImage(filename,int(width),int(height),0)
            os.rename(f"outputs/resized{res}{filename}",f"inputs/resized{res}{filename}")

        for res in resolutions:
            if codec == "vp8":
                self.convertToVP8(f"resized{res}{filename}")
                os.rename(f"outputs/vp8resized{res}{filename[:-4]}.webm",f"outputs/ladder/vp8resized{res}{filename[:-4]}.webm")

            elif codec == "vp9":
                self.convertToVP9(f"resized{res}{filename}")
                os.rename(f"outputs/vp9resized{res}{filename[:-4]}.webm",f"outputs/ladder/vp9resized{res}{filename[:-4]}.webm")

            elif codec == "h265":
                self.convertToH265(f"resized{res}{filename}")
                os.rename(f"outputs/h265resized{res}{filename}",f"outputs/ladder/h265resized{res}{filename}")

            elif codec == "av1":
                self.convertToAV1(f"resized{res}{filename}")
                os.rename(f"outputs/av1resized{res}{filename[:-4]}.mkv",f"outputs/ladder/av1resized{res}{filename[:-4]}.mkv")
            os.remove(f"inputs/resized{res}{filename}")
        shutil.make_archive(f"ladder{codec}{filename}", 'zip', "outputs/ladder")
        shutil.rmtree("outputs/ladder")
        return True
    def packageHLSAVCAAC(filename):
        command = f"ffmpeg -i inputs/{filename} -c:v libx264 -c:a aac -b:a 128k -ac 2 -hls_time 10 -hls_list_size 0 -f hls -y outputs/hls{filename[:-4]}.m3u8"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def packageDASHVP9AAC(filename):
        command = f"ffmpeg -i inputs/{filename} -c:v libvpx-vp9 -c:a aac -f dash -y outputs/dash{filename[:-4]}.mpd"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
   
                
#task 6
class DCT:
    def convert(filename): 
        with Image.open(f"inputs/{filename}") as img:
            grayscale = img.convert('L')
            img_array = np.array(grayscale, dtype=np.uint8)
        dct_image = dctn(img_array, norm = 'ortho')
        return dct_image

    def decoder(dct_image,filename):
        estimated_image = idctn(dct_image, norm = 'ortho')
        estimated_image_uint8 = np.clip(estimated_image, 0, 255).astype(np.uint8)
        im = Image.fromarray(estimated_image_uint8)
        im.save(f"outputs/dct{filename}")
    
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
            
