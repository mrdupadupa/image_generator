# Generator of images with geometric shapes
Generator of images containing geometric shapes based on the skimage image generator.
It was used to generate dataset with 3 classes:


Core:

Rectangles:10%, Triangles:10%, Circles:80%


Halo:

Rectangles:45%, Triangles:45%, Circles:10%


Control:

Rectangles:50% Triangles:50%


Example of use (how it was done):

```

new_list = [i for i in range(15000)]

#Generating images for Core class (circles with 10% triangles and rectangles)

for i in range(len(new_list)):

    new_list[i], _ = random_shapes((1280, 1280), min_shapes=3, max_shapes=4, min_size=20, scenario='SHAPEGENERATOR_ALL_CORE', allow_overlap=False, multichannel=False)
    
    plt.imshow(new_list[i])
    matplotlib.image.imsave("/lustre/ssd/ws/anpo879a-master_thesis/master_thesis/data_set2/quasi_core/%s.png" % ((i)), new_list[i], cmap="Greys")
    


#Generating images for Halo class (triangles and rectangles with 10% of circles)

for i in range(len(new_list)):

    new_list[i], _ = random_shapes((1280, 1280), min_shapes=3, max_shapes=4, min_size=20, scenario='SHAPEGENERATOR_ALL_HALO', allow_overlap=False, multichannel=False)
    
    plt.imshow(new_list[i])
    matplotlib.image.imsave("/lustre/ssd/ws/anpo879a-master_thesis/master_thesis/data_set2/quasi_halo/%s.png" % ((i)), new_list[i], cmap="Greys")
    


#Generating images for Control class (triangles and rectangles)

for i in range(len(new_list)):

    new_list[i], _ = random_shapes((1280, 1280), min_shapes=3, max_shapes=4, min_size=20, scenario='SHAPEGENERATOR_R_T', allow_overlap=False, multichannel=False)
    
    plt.imshow(new_list[i])
    matplotlib.image.imsave("/lustre/ssd/ws/anpo879a-master_thesis/master_thesis/data_set2/quasi_control/%s.png" % ((i)), new_list[i], cmap="Greys")
    ```
