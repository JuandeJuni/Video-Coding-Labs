import shutil
from typing import Union
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from first_seminar import VideoEncoder, DCT, DWT


app = FastAPI()


@app.get("/")
def read_root():
    return "Welcome to the Video (image) Encoder API!, we are Raquel Maldonado (241519) and Juande Gutierrez (241573)"


@app.get("/upload-image-form", response_class=HTMLResponse)
async def upload_image_form():
    """
    Returns an HTML form for uploading an image.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload Image</title>
    </head>
    <body>
        <h1>Upload an Image</h1>
        <form action="/upload-image/" enctype="multipart/form-data" method="post">
            <input type="file" name="image" accept="image/*, video/*">
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/upload-image/")
async def upload_image(image: UploadFile = File(...)):
    """
    Receives an image and saves it to the server, then returns its details.
    """
    if image.content_type not in ["image/jpeg", "image/png", "image/jpg", "video/mp4", "video/quicktime","video/x-msvideo", "video/x-matroska" ]:
        return {"error": "Unsupported file type. Please upload a JPEG or PNG image or Video."}

    # Save the file
    file_path = f"inputs/{image.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return "Success"
    
@app.get("/resize-image")
async def resize_image(filename: str,width: int,height: int,compression: int):
    VideoEncoder.resizeImage(filename,width,height,compression)
    return FileResponse(f"outputs/resized{filename}")

@app.get("/blackandwhite")
async def black_and_white(filename: str,compression: int):
    VideoEncoder.color_to_bw(filename,compression)
    return FileResponse(f"outputs/bw{filename}")

@app.get("/serpentine")
async def serpentine(filename: str):
    return VideoEncoder.serpentine(filename)

@app.get("/runlength")
async def runlength(string: str):
    b = bytearray()
    b.extend(map(ord, string))
    return VideoEncoder.runlength_encode(b)

@app.get("/dct")
async def dct(filename: str):
    dctImage = DCT.convert(filename)
    dctEstimatedImage = DCT.decoder(dctImage,filename)
    return FileResponse(f"outputs/dct{filename}")

@app.get("/RGBtoYUV")
async def RGBtoYUV(r: int,g: int,b: int):
    return VideoEncoder.RGBtoYUV(r,g,b)    
    
    
@app.get("/YUVtoRGB")
async def YUVtoRGB(y: int,u: int,v: int):
    return VideoEncoder.YUVtoRGB(y,u,v)

@app.get("/chroma-subsampling")
async def ChromaSubsampling(filename: str,chroma_subsampling: str):
    VideoEncoder.chromaSubsampling(filename,chroma_subsampling)
    return FileResponse(f"outputs/{chroma_subsampling}{filename}")

@app.get("/get-info")
async def GetInfo(filename: str):
    result = VideoEncoder.getInfo(filename)
    return result

@app.get("/package-video")
async def PackageVideo(filename: str):
    nameOnly = filename[:-4]
    VideoEncoder.cutVideo(filename,"00:00:00","00:00:20")
    VideoEncoder.getMonoAAC(f"cut{filename}")
    VideoEncoder.getMP3Stereo(f"cut{filename}","96k")
    VideoEncoder.getAC3(f"cut{filename}")
    VideoEncoder.packageMP4(f"cut{filename}",f"monocut{nameOnly}.aac",f"stereocut{nameOnly}.mp3",f"ac3cut{nameOnly}.ac3")
    return FileResponse(f"outputs/packagedcut{nameOnly}.mp4")

@app.get("/number-of-tracks")
async def NumberOfTracks(filename: str):
    result = VideoEncoder.getInfo(filename)
    nbtracks = result['format']['nb_streams']
    typeOfTracks = []
    codecOfTracks = []
    for i in result["streams"]:
        typeOfTracks.append(i["codec_type"])
        codecOfTracks.append(i["codec_name"])
    resultJson = {
        "Number of tracks": nbtracks,
        "Type of tracks": typeOfTracks,
        "Type of codecs": codecOfTracks
    }

    return resultJson

@app.get("/get-motion")
async def GetMotion(filename: str):
    VideoEncoder.getMotion(filename)
    return FileResponse(f"outputs/motion{filename[:-4]}.mp4")

@app.get("/get-histogram")
async def GetHistogram(filename: str):
    VideoEncoder.getHistogram(filename)
    return FileResponse(f"outputs/histogram{filename}")

