import random
from vectormath import VectorMath
import operator

class History(object):
    def __init__(self, num_timepoints, vector_length, classes):
        self._num_timepoints = num_timepoints
        self._vector_length = vector_length
        self._classes = classes
        
        self._memory = {}
        for class_label in classes:
            self._memory[class_label] = self.create_random_memory()
            
    def create_random_memory(self):
        return [[random.random() for i in range(self._vector_length)] for j in range(self._num_timepoints)]
    
    def get_most_likely_class(self, vector, update_memory=True, target_class=None):
        similarities = self.get_similarities(vector)
        similarity_averages = self.get_similarity_averages(similarities)
        most_likely = max(similarity_averages.iteritems(), key=operator.itemgetter(1))
        most_likely_class = most_likely[0]
        most_likely_similarity_avg = most_likely[1]
        if update_memory:
            self.update_memory(vector, most_likely_class, similarities[most_likely_class])
        prediction = {}
        prediction['char'] = most_likely_class
        prediction['top_similarity'] = most_likely_similarity_avg
        prediction['avg_similarity'] = VectorMath.average(similarity_averages.values())
        if target_class != None:
            if most_likely_class == target_class:
                prediction['is_output_correct'] = 1
            else:
                prediction['is_output_correct'] = 0
            prediction['target_similarity'] = similarity_averages[target_class]
        else:
            prediction['target_similarity'] = most_likely_similarity_avg
            prediction['is_output_correct'] = 0
        return prediction
    
    def get_similarity(self, vector, class_label):
        return [VectorMath.cosine_similarity(vector, memory) for memory in self._memory[class_label]]
    
    def get_similarity_average(self, similarity):
        return VectorMath.average(similarity)
                
    def get_similarities(self, vector):
        similarities = {}
        for class_label, memories in self._memory.iteritems():
            similarities[class_label] = [VectorMath.cosine_similarity(vector, memory) for memory in memories]
        return similarities
    
    def get_similarity_averages(self, similarities):
        similarity_averages = {}
        for class_label, similarity in similarities.iteritems():
            similarity_averages[class_label] = VectorMath.average(similarity)
        return similarity_averages
    
    def update_memory(self, vector, class_label, similarity):
        self._memory[class_label][similarity.index(min(similarity))] = vector