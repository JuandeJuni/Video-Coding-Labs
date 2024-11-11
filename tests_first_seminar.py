from first_seminar import VideoEncoder

print(VideoEncoder.RGBtoYUV(222,107,238))
print(VideoEncoder.YUVtoRGB(150,168,169))
VideoEncoder.resizeImage("RaquelJuande.jpeg",4,4,30)
VideoEncoder.serpentine("resizedRaquelJuande.jpeg")
VideoEncoder.color_to_bw("RaquelJuande.jpeg","bwRaquelJuande.jpeg")