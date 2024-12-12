
# Image Encoder API

The main idea of this project is building a docker container that hosts an API with multiple endpoints that perform image encoding tasks.




## Installation

Build the docker image and run the a container.
```bash
  docker compose build
  docker compose up
```

    
## Usage/Examples

The access the API you should go to port 8000
```
localhost:8000 or 127.0.0.1:8000
```


## API Reference

#### Upload your image
```http
  GET /upload-image-form
```

#### Resize image

```http
  GET /resize-image
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |
| `width`      | `int` | **Required**. Width of the resized image |
| `height`      | `int` | **Required**. Height of the resized image |
| `compression`      | `int` | **Required**. Value between 1-32 |

#### Black and White

```http
  GET /blackandwhite
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |
| `compression`      | `int` | **Required**. Value between 1-32 |

#### Serpentine Image Reader
```http
  GET /serpentine
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Run Length Encoding
```http
  GET /runlength
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `string`      | `string` | **Required**. String of values you want to encode |


#### DCT Estimation
```http
  GET /dct
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### RGB to YUV
```http
  GET /RGBtoYUV
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `r`      | `int` | **Required**. Red channel value |
| `g`      | `int` | **Required**. Green channel value |
| `b`      | `int` | **Required**. Blue channel value |

#### YUV to RGB
```http
  GET /YUVtoRGB
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `y`      | `int` | **Required**. Luminance channel value |
| `u`      | `int` | **Required**. Chroma1 channel value |
| `v`      | `int` | **Required**. Chroma2 channel value |

#### Chroma Subsampling 
```http
  GET /chroma-subsampling
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |
| `chroma_subsampling`      | `string` | **Required**. You can choose any method name from the list "listChromaSubsampling.txt" |

#### Get Information 
```http
  GET /getInfo
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Package Video 
```http
  GET /package-video
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Number of tracks 
```http
  GET /number-of-tracks
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Get motion
```http
  GET /get-motion
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Get histogram
```http
  GET /get-histogram
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Convert to vp8
```http
  GET /convert-to-vp8
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Convert to vp9
```http
  GET /convert-to-vp9
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Convert to h265
```http
  GET /convert-to-h265
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Convert to av1
```http
  GET /convert-to-av1
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |

#### Encoding ladder
```http
  GET /encoding-ladder
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `filename`      | `string` | **Required**. Name of the file you uploaded |
| `codec`      | `string` | **Required**. choose between vp8,vp9,h265,av1 |