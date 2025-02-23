import torch

dir_data = dir(torch.utils.data)
dir_data = dir(torch.utils.data.Dataset)
dir_data = dir(torch.cuda)
dir_data = dir(torch.cuda.is_available())
help(torch.cuda.is_available)
print(dir_data)






