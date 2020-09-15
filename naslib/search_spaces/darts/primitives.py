import torch
import torch.nn as nn

from ..core.primitives import AbstractPrimitive


class FactorizedReduce(AbstractPrimitive):
    """
    Whatever this is, it replaces the identity when stride=2
    """

    def __init__(self, C_in, C_out, affine=False):
        super(FactorizedReduce, self).__init__()
        assert C_out % 2 == 0
        self.relu = nn.ReLU(inplace=False)
        self.conv_1 = nn.Conv2d(C_in, C_out // 2, 1, stride=2, padding=0, bias=False)
        self.conv_2 = nn.Conv2d(C_in, C_out // 2, 1, stride=2, padding=0, bias=False)
        self.bn = nn.BatchNorm2d(C_out, affine=affine)

    def forward(self, x, edge_data):
        x = self.relu(x)
        out = torch.cat([self.conv_1(x), self.conv_2(x[:, :, 1:, 1:])], dim=1)
        out = self.bn(out)
        return out
    
    def get_embedded_ops(self):
        return None

