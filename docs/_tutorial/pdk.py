import os 
import sys

parentdir = os.getcwd()
sys.path.insert(0, parentdir)
from sample_pdk import technology
import sample_pdk.components as cs
from draw import draw
from palgds.circuit import Circuit

os.chdir(os.path.dirname(os.path.abspath(__file__)))

development = True
#path = os.path.dirname(os.path.abspath(__file__)) + "/"
path = "../_source_files/"


ybranch = cs.YBranch()
if development:
    draw(ybranch, path, scaling=12)


splitter = Circuit(name='Splitter',
              pcells={"ybranch1": ybranch, "ybranch2": ybranch, "ybranch3":ybranch},
              translations={"ybranch1": (0, 0),
                            "ybranch2": (30, 15),
                            "ybranch3": (30, -15)
                            },
              links=[{"from": ("ybranch1", "out1"), "to": ("ybranch2", "in")},
                     {"from": ("ybranch1", "out2"), "to": ("ybranch3", "in")},
                     ],
              )
# end of splitter

if development:
       draw(splitter, path, scaling=9)