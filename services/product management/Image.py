import matplotlib.pyplot as plt
import cv2

class Image:
    def __init__(self, file_location, id=0):
        self.id = id
        self.file_location = file_location

    def display(self):
        img = cv2.imread(self.file_location)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img)
        plt.axis("off")
        plt.show()