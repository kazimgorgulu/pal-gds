import os
import palgds.base_cells as bc


gds_path = os.path.join(os.path.dirname(__file__), "gds\\")

class YBranch(bc.GDSCell):
    """"""
    def __init__(self):
        super().__init__(name="YBranch", filename=gds_path+'YBranch.gds', ports_filename=gds_path+"YBranch.txt")




