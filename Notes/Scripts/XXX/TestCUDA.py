import torch

def check_cuda_version():
    if torch.cuda.is_available():
        print("CUDA可用")
        print("CUDA版本:", torch.version.cuda)
    else:
        print("CUDA不可用")

# 在文件的适当位置调用该函数
check_cuda_version()
