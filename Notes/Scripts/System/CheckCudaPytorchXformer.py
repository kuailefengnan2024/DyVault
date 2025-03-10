import torch
import xformers

print("PyTorch Version:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available())
print("CUDA Version:", torch.version.cuda)
print("PyTorch Installation Path:", torch.__file__)

print("xFormers Version:", xformers.__version__)
print("xFormers Installation Path:", xformers.__file__)
