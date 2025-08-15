from diffab.tools.runner.design_for_pdb import args_from_cmdline, design_for_pdb
import os
hmmscan_directory = '/data/yuangang/miniforge3/envs/diffab/bin'
os.environ['PATH'] = hmmscan_directory + ':' + os.environ['PATH']

if __name__ == '__main__':
    design_for_pdb(args_from_cmdline())
