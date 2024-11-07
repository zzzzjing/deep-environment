# -*- coding: utf-8 -*-

# 导入 Portal 和 ProtoGENI 库
import geni.portal as portal
import geni.rspec.pg as pg

# 创建一个 Portal 上下文
pc = portal.Context()

# 创建一个 RSpec 请求对象
request = pc.makeRequestRSpec()

# 定义节点配置
# 使用具有 GPU 的节点类型 "ibm8335"
node = request.RawPC("gpu-node")
node.hardware_type = "ibm8335"  # 修改为您的 GPU 节点类型 ibm8335

# 设置节点的操作系统镜像
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD"  # 使用 Ubuntu 20.04

# 定义启动时自动安装深度学习环境的脚本
setup_script = """
#!/bin/bash

# 更新系统包
sudo apt-get update -y

# 安装基本工具
sudo apt-get install -y build-essential gcc g++ make

# 安装 Python 和 pip
sudo apt-get install -y python3 python3-pip

# 安装 NVIDIA 驱动和 CUDA（具体版本可能需要根据硬件进行调整）
wget https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_520.61.05_linux.run
sudo sh cuda_11.7.1_520.61.05_linux.run --silent --toolkit --samples

# 配置 CUDA 环境变量
echo "export PATH=/usr/local/cuda-11.7/bin:$PATH" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/cuda-11.7/lib64:$LD_LIBRARY_PATH" >> ~/.bashrc
source ~/.bashrc

# 安装 cuDNN
# 下载 cuDNN 压缩包并解压到 CUDA 路径下（需要自行下载并上传到节点）
# 示例：tar -xzvf cudnn-11.7-linux-x64-v8.1.1.33.tgz -C /usr/local/cuda

# 安装深度学习框架
pip3 install torch torchvision torchaudio tensorflow

# 验证安装
python3 -c "import torch; print('PyTorch version:', torch.__version__)"
python3 -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

echo "深度学习环境安装完成"
"""

# 将安装脚本添加到节点服务
node.addService(pg.Execute(shell="bash", command=setup_script))

# 打印 RSpec
pc.printRequestRSpec(request)
