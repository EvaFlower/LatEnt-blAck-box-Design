#!/bin/bash
#PBS -N WD
#PBS -l select=1:ncpus=14:ngpus=1:mem=470gb
#PBS -l walltime=30:00:00
#PBS -P 13003948
#PBS -q normal
#PBS -o my_output.txt  
#PBS -e my_error.txt   
#PBS -j oe             


module load cuda/11.8.0
module load miniforge3
conda activate diffab

cd file_address/

# Guiding design: Sampling by property
for i in {0..18}; do
  python design_testset.py $i --config ./configs/test/codesign_single_ddg.yml --sample_step_mode min --sample_step_num 20 --sample_step_period 1
done
python results_sumarization.py  --root_dir "results/codesign_single_ddg_min/"

for i in {1..18}; do
  python design_testset.py $i --config ./configs/test/codesign_single_hydro.yml --sample_step_mode softmax --sample_step_num 20 --sample_step_period 1
done
python results_sumarization.py  --root_dir "results/codesign_single_hydro_softmax/"


# Guiding design: Sampling by property
for i in {0..18}; do
  python design_testset.py $i --config ./configs/test/codesign_single_ddg_and_hydro.yml --sample_step_mode min --sample_step_num 20 --sample_step_period 1 --property_weight 0.5
done
python results_sumarization.py  --root_dir "results/codesign_single_ddg_and_hydro_min_0.5/"



for i in 1 2 4 8 16 32; do

  python design_query_efficient.py --config ./configs/test/codesign_single_ddg.yml --tag partial --opt_type BestN --sample_step_mode min --sample_step_num $i --sample_step_period 1
  python results_sumarization.py  --root_dir "results/query_efficient_BestN/codesign_single_ddg_partial_min_${i}/5xku_C_B_A/"

  python design_query_efficient.py --config ./configs/test/codesign_single_hydro.yml --tag partial --opt_type BestN --sample_step_mode min --sample_step_num $i --sample_step_period 1
  python results_sumarization.py  --root_dir "results/query_efficient_BestN/codesign_single_hydro_partial_min_${i}/5xku_C_B_A/"

  python design_query_efficient.py --config ./configs/test/codesign_single_ddg.yml --tag partial --opt_type BestN --sample_step_mode softmax --sample_step_num $i --sample_step_period 1
  python results_sumarization.py  --root_dir "results/query_efficient_BestN/codesign_single_ddg_partial_softmax_${i}/5xku_C_B_A/"

  python design_query_efficient.py --config ./configs/test/codesign_single_hydro.yml --tag partial --opt_type BestN --sample_step_mode softmax --sample_step_num $i --sample_step_period 1
  python results_sumarization.py  --root_dir "results/query_efficient_BestN/codesign_single_hydro_partial_softmax_${i}/5xku_C_B_A/"
done