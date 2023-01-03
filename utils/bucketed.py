import random

from models import FloatColor

class BucketedUtils(object):
    @classmethod
    def get_color(cls, x:float, y:float, colors:list[FloatColor], divergance:float=0):
        buckets = len(colors)
        bucket_width = 2/buckets
        color_prob = []

        for i in range(buckets):
            color_prob.append(None)

        for i in range(buckets):
            color_prob[i] = abs(random.normalvariate(bucket_width * (i + 0.5), divergance) - (x + y))

        max_prob = min(color_prob)
        for i in range(buckets):
            if max_prob == color_prob[i]:
                return colors[i]
        return (0, 0, 0)