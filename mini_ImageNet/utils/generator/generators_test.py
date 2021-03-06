"""
This code based on codes from https://github.com/tristandeleu/ntm-one-shot \
                              and https://github.com/kjunelee/MetaOptNet
"""
import numpy as np
import random
import pickle as pkl
import subprocess
import zipfile

def extract(filename):
    zipFile_ = '../../../miniImageNet.zip'
    subprocess.call(['mkdir', '../data/miniImageNet'])
    dest = '../data/miniImageNet'
    archive = zipfile.ZipFile(zipFile_)
    for file in archive.namelist():
        if file.startswith(filename.split('/')[-1]):
            archive.extract(file, dest)

def remove(filename):
    filepath = '../data/miniImageNet/' + filename.split('/')[-1]
    subprocess.call(['rm', filepath])

class miniImageNetGenerator(object):

    def __init__(self, data_file, nb_classes=5, nb_samples_per_class=15,
                  max_iter=None, xp=np):
        super(miniImageNetGenerator, self).__init__()
        self.data_file = data_file
        self.nb_classes = nb_classes
        self.nb_samples_per_class = nb_samples_per_class
        self.max_iter = max_iter
        self.xp = xp
        self.num_iter = 0
        self.data = self._load_data(self.data_file)

    def _load_data(self, data_file):
        dataset = self.load_data(data_file)
        data = dataset['data']
        labels = dataset['labels']
        label2ind = self.buildLabelIndex(labels)

        return {key: np.array(data[val]) for (key, val) in label2ind.items()}

    def load_data(self, data_file):
        try:
            extract(data_file)
            with open(data_file, 'rb') as fo:
                data = pkl.load(fo)
                remove(data_file)
            return data
        except:
            with open(data_file, 'rb') as f:
                u = pkl._Unpickler(f)
                u.encoding = 'latin1'
                data = u.load()
            return data

    def buildLabelIndex(self, labels):
        label2inds = {}
        for idx, label in enumerate(labels):
            if label not in label2inds:
                label2inds[label] = []
            label2inds[label].append(idx)

        return label2inds


    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if (self.max_iter is None) or (self.num_iter < self.max_iter):
            self.num_iter += 1
            images, labels = self.sample(self.nb_classes, self.nb_samples_per_class)

            return (self.num_iter - 1), (images, labels)
        else:
            raise StopIteration()

    def sample(self, nb_classes, nb_samples_per_class):
        sampled_characters = random.sample(self.data.keys(), nb_classes)
        labels_and_images = []
        for (k, char) in enumerate(sampled_characters):
            _imgs = self.data[char]
            _ind = random.sample(range(len(_imgs)), nb_samples_per_class)
            labels_and_images.extend([(k, self.xp.array(_imgs[i]/np.float32(255).flatten())) for i in _ind])
        arg_labels_and_images = []
        for i in range(self.nb_samples_per_class):
            for j in range(self.nb_classes):
                arg_labels_and_images.extend([labels_and_images[i+j*self.nb_samples_per_class]])

        labels, images = zip(*arg_labels_and_images)
        return images, labels

