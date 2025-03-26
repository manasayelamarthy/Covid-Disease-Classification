import cv2
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


class covidDataset():
    def __init__(self, root_dir):
        self.path = root_dir


    def load_path(self):
        """
        Load image paths from root dir having 3 different classes.
        """
        self.imagePaths = {}
        num_classes = os.listdir(self.path)  
        self.imagePath = {i : [] for i in num_classes}
        for class_dir in num_classes:  
            class_folder = os.path.join(self.path, class_dir) 
            
            if os.path.isdir(class_folder):  
                for image_file in os.listdir(class_folder): 
                    image_path = os.path.join(class_folder, image_file) 
                    self.imagePath[class_dir].append(image_path)

        return self.imagePaths


    def plot_images(self):
            """
            Plot images from the dataset
            """
            image_paths = self.load_path()

            covidImage  = cv2.imread(image_paths["Covid"][0], cv2.IMREAD_GRAYSCALE)
            NormalImage = cv2.imread(image_paths["Normal"][0], cv2.IMREAD_GRAYSCALE)
            viralPImage = cv2.imread(image_paths["viral Pneumonia"][0], cv2.IMREAD_GRAYSCALE)

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
        image_paths = self.load_path()
        images = []
        labels = []
        for i in image_paths:
            for image_path in image_paths[i]:
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                image = cv2.resize(image, (256, 256))
                image = image/255.0
                images.append(image)
                labels.append(i)

        images = np.array(images)
        labels = np.array(labels)

        return images, labels

    def labels_numeric(self):
        """
        Convert labels to numeric
        """
        labels = self.load_data()[1]
        labels_numeric = pd.get_dummies(labels)
        labels_numeric = labels_numeric.values.argmax(1)
        return labels_numeric


if __name__ =="__main__":
    datapath = "D:/Projects/Covid Image Dataset/data/covid/Covid19-dataset/train"
    dataset = covidDataset(root_dir = datapath)
    print(dataset.imagePaths)