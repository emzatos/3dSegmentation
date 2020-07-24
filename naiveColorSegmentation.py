# go through each pixel
# add to map
# if within color range, add to segment
# continue???



import math
from PIL import Image
from functools import reduce
import operator
from random import randint

distance = lambda a, b: math.sqrt(reduce(operator.add, map(lambda ab: (ab[0] - ab[1])**2, zip(a, b))))

vector_add = lambda v, w: tuple(map(lambda ab: ab[0] + ab[1], zip(v, w)))

image = Image.open("me.jpg")

segmented_image = Image.new('RGB', image.size, "black")
segment_pixels = segmented_image.load()

rgb_im = image.convert('RGB')

color_map = set()
max_dist = 50
dimensions = image.size



def color_segmentation():
    for x in range(dimensions[0]):
        print(x)
        for y in range(dimensions[1]):

            color = image.getpixel((x,y))

            for label in color_map:
                if distance(color, label) <= max_dist:
                    segment_pixels[x, y] = label
                    break
            else:
                color_map.add(color)
                segment_pixels[x, y] = color

    segmented_image.show()
        

def kmeans():
    k = 3
    centroids = [(randint(0, 255),randint(0, 255),randint(0, 255)) for x in range(k)]
    for i in range(10):
        print(i)
        assigned_pixels = [[] for x in range(k)]
        for x in range(dimensions[0]):
            for y in range(dimensions[1]):
                color = image.getpixel((x,y))
                min_dist = 10000000
                centroid = centroids[0]
                for label in centroids:
                    cur_dist = distance(color, label)
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        centroid = label
                
                segment_pixels[x,y] = centroid
                # if i == 4:
                #     print(i, segment_pixels[x,y])
                assigned_pixels[centroids.index(centroid)].append(color)
        
        for idx, data in enumerate(assigned_pixels):
            if len(data) == 0:
                continue
            centroids[idx] = reduce(vector_add, data)
            centroids[idx] = tuple(x // len(data) for x in centroids[idx])

    segmented_image.show()

kmeans()


                    