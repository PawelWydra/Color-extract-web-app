import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster


class ColorList:
    def __init__(self, image):
        self.num_clusters = 10
        self.image = image

    def color_list(self):
        im = Image.open(self.image)
        im = im.resize((150, 150))  # optional, to reduce time
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

        codes, dist = scipy.cluster.vq.kmeans(ar, self.num_clusters)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
        counts, bins = scipy.histogram(vecs, len(codes))  # count occurrences

        index_max = scipy.argmax(counts)  # find most frequent
        colours = []
        for code in range(len(codes)):
            peak = codes[code]
            colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
            colours.append(colour)
        return colours
