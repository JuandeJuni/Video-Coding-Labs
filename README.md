
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