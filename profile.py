# -*- coding: utf-8 -*-

# 导入 Portal 和 ProtoGENI 库
import geni.portal as portal
import geni.rspec.pg as pg

# 创建一个 Portal 上下文
pc = portal.Context()

# 创建一个 RSpec 请求对象
request = pc.makeRequestRSpec()

# 定义节点配置
node = request.RawPC("gpu-node")
node.hardware_type = "ibm8335"  # 修改为您的 GPU 节点类型 ibm8335

# 设置节点的操作系统镜像
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD"

# 定义启动时自动安装深度学习环境的脚本
setup_script = (
    "#!/bin/bash\n"
    "sudo apt-get update -y && "
    "sudo apt-get install -y build-essential gcc g++ make && "
    "sudo apt-get install -y python3 python3-pip && "
    "wget https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_520.61.05_linux.run && "
    "sudo sh cuda_11.7.1_520.61.05_linux.run --silent --toolkit --samples && "
    "echo 'export PATH=/usr/local/cuda-11.7/bin:$PATH' >> ~/.bashrc && "
    "echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.7/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc && "
    "source ~/.bashrc && "
    "pip3 install torch torchvision torchaudio tensorflow && "
    "python3 -c \"import torch; print('PyTorch version:', torch.__version__)\" && "
    "python3 -c \"import tensorflow as tf; print('TensorFlow version:', tf.__version__)\" && "
    "echo '深度学习环境安装完成'"
)

# 将安装脚本添加到节点服务
node.addService(pg.Execute(shell="bash", command=setup_script))

# 打印 RSpec
pc.printRequestRSpec(request)
