from diffab.tools.runner.design_for_ablation import main
import os
hmmscan_directory = '/data/yuangang/miniforge3/envs/diffab/bin'
os.environ['PATH'] = hmmscan_directory + ':' + os.environ['PATH']
if __name__ == '__main__':
    main()
