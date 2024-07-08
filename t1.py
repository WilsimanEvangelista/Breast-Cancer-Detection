import json
list_Images = "[\"07/08/2024 05:46:13 PM_Img.jpg\", \"07/08/2024 05:46:19 PM_Img.jpg\", \"07/08/2024 05:46:24 PM_Img.jpg\", \"07/08/2024 05:46:30 PM_Img.jpg\"]"
print(json.loads(list_Images))
new_list_images = []
for i in list_Images:
    new_list_images.append(i.replace("\"","\'"))
print(new_list_images)