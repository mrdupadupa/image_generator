# Generator of images with geometric shapes
Generator of images containing geometric shapes.
Generator is based on the skimage image generator.
Generator allows to generate images on of 3 following classes:


* `core`: Rectangles:10%, Triangles:10%, Circles:80%


* `halo`: Rectangles:45%, Triangles:45%, Circles:10%


* `control`: Rectangles:50% Triangles:50%


Example of usage:

```
#Install requirements:
pip install -r requirements.txt

#Generate images
python image_generator_complex_scenarious.py --types "halo"
```
