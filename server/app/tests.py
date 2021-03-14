from django.test import TestCase
import torch
# Create your tests here.
print( torch.cuda.is_available())
print(torch.__version__)
import sys
print(sys.executable)
print(sys.version)
print(sys.version_info)

torch.zeros(1).cuda()