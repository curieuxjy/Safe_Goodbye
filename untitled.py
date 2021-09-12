from dataset import CustomImageDataset

a = CustomImageDataset("D:\\work\\train\\label", "D:\\work\\train\\image")
print(a.__len__())