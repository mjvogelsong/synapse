import math

class VectorMath(object):
    
    @staticmethod
    def cosine_similarity(v1, v2):
        sumxx = 0
        sumxy = 0
        sumyy = 0
        for i in range(len(v1)):
            x = v1[i]; y = v2[i]
            sumxx += x*x
            sumyy += y*y
            sumxy += x*y
        denom = math.sqrt(sumxx*sumyy)
        if denom > 0:
            return sumxy/math.sqrt(sumxx*sumyy)
        else:
            return 0.0
    
    @staticmethod
    def average(sequence):
        return float(sum(sequence)) / len(sequence)
        