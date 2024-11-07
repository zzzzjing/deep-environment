# -*- coding: utf-8 -*-

# Import the Portal and ProtoGENI libraries
import geni.portal as portal
import geni.rspec.pg as pg

# Create a Portal context
pc = portal.Context()

# Create a Request object to start building the RSpec
request = pc.makeRequestRSpec()

# Define node configuration
node = request.RawPC("gpu-node")
node.hardware_type = "ibm8335"  # Set to your GPU node type "ibm8335"

# Set the node's OS image
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD"  # Use Ubuntu 20.04

# Define a script to automatically install the deep learning environment at startup
setup_script = (
    "#!/bin/bash\n"
    "sudo apt-get update -y && "
    "sudo apt-get install -y build-essential gcc g++ make && "
    "sudo apt-get install -y python3 python3-pip && "
    "wget https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_520.61.
