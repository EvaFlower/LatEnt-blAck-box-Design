# # Property-unconditioned design
# # Sample 7DK2_AB_C
python design_pdb.py --pdb_path ./data/examples/7DK2_AB_C.pdb --config ./configs/test/codesign_single.yml --tag partial 
# Evaluation: AAR, RMSD, Hydropathy Score, and Predicted ddG (the option --no_energy prevents the computation of Rosetta ddG) for all samples use:
python single_results_sumarization.py  --root_dir "/data/yuangang/AD/antibody-diffusion-properties/results/examples/codesign_single_partial/7DK2_AB_C.pdb"

# Guiding design: Sampling by property
# Sample 7DK2_AB_C
python design_pdb.py --pdb_path ./data/examples/7DK2_AB_C.pdb --config ./configs/test/codesign_single_ddg_and_hydro.yml --tag partial --sample_step_mode min --sample_step_num 20 --sample_step_period 1 --property_weight 0.5 --normalize Normalize
# Evaluation: AAR, RMSD, Hydropathy Score, and Predicted ddG (the option --no_energy prevents the computation of Rosetta ddG) for all samples use:
python single_results_sumarization.py  --root_dir "results/examples/codesign_single_ddg_and_hydro_partial_0.5_Normalize/7DK2_AB_C.pdb"
