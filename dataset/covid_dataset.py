import cv2
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import logging

#initialize logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok = True)

logger = logging.getLogger("data Ingestion")
logger.setLevel(logging.DEBUG)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.DEBUG)

file_path = os.path.join(log_dir, 'data Ingestion.log')
file_logger = logging.FileHandler(file_path)
file_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')
console_logger.setFormatter(formatter)
file_logger.setFormatter(formatter)

logger.addHandler(console_logger)
logger.addHandler(file_logger)



class covidDataset():
    def __init__(self, root_dir):
        self.path = root_dir
        self.imagePaths = {}


    def load_paths(self):
        """
        Load image paths from root dir having 3 different classes.
        """
        try: 
            num_classes = os.listdir(self.path)  
            self.imagePaths = {classes : [] for classes in num_classes}
            for classes in num_classes:  
                class_dir = self.path + classes
                
                if os.path.isdir(class_dir):
    
                    for image_file in os.listdir(class_dir): 
                        image_path = class_dir +  '/' + image_file 
                        self.imagePaths[classes].append(image_path)
            logger.debug("loaded imagePaths with 3 classes")
            return self.imagePaths
        except Exception as e:
            logger.error('unable to load imagePaths %s', e)


    def plot_images(self):
            """
            Plot images from the dataset
            """
            image_paths = self.load_paths()

            covidImage  = cv2.imread(image_paths["Covid"][0], cv2.IMREAD_GRAYSCALE)
            NormalImage = cv2.imread(image_paths["Normal"][0], cv2.IMREAD_GRAYSCALE)
            viralPImage = cv2.imread(image_paths["Viral Pneumonia"][0], cv2.IMREAD_GRAYSCALE)

            _,axes =  plt.subplots(1, 3, figsize = (10, 5) )
            axes[0].imshow(covidImage, cmap = 'gray')
            axes[0].set_title("covidImage")
            axes[0].axis("off")

            axes[1].imshow(NormalImage, cmap = 'gray')
            axes[1].set_title("NormalImage")
            axes[1].axis("off")

            axes[2].imshow(viralPImage, cmap = 'gray')
            axes[2].set_title("viralPImage")
            axes[2].axis("off")

            plt.show()


    def load_data(self):
        """
        Load images from the dataset 
        """
        try :

            image_paths = self.load_paths()
            images = []
            labels = []
            for i in image_paths:
                for image_path in image_paths[i]:
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    image = cv2.resize(image, (224, 224))
                    image = image/255.0
                    images.append(image)
                    labels.append(i)

            images = np.array(images)
            labels = np.array(labels)

            logger.debug('loaded images and lables list')
            return images, labels
        except Exception as e:
            logger.error('unable to get images,labels lists  %s', e)

    def labels_numeric(self):
        """
        Convert labels to numeric
        """
        try :
            labels = self.load_data()[1]
            labels_numeric = pd.get_dummies(labels)
            labels_numeric = labels_numeric.values.argmax(1)
            logger.debug('converted labels to numeric values using one hot encoding')
            return labels_numeric
            
        except Exception as e:
            logger.error('error in converting into labels to numerical values %s', e)



if __name__ =="__main__":
    datapath = "data/Covid19-dataset/train/"
    dataset = covidDataset(root_dir = datapath)
    dataset.labels_numeric()

    
