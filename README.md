# LatEnt blAck-box Design (LEAD)

This repository contains the code for the paper: "Generative Co-Design of Antibody Sequences and Structures via Black-Box Guidance in a Shared Latent Space (IJCAI 25)".

![overview](./assets/framework.png)
*Figure: Overall framework. **Left panel** describes the whole process of our guided sampling. **Right panel** details the black-box guidance incorporated in the shared latent space of sequence and structure.*


## Unconditional Sampling (DiffAb) & Property guided Sampling (our LEAD)

### Environment

```bash
conda env create -f env.yaml -n diffab
conda activate diffab
```

### Script for Single sample
```bash
bash test_run.sh
```
### Script for Test set
```bash
bash testset_run.sh
```

### Datasets and model weights

Protein structure data can be downloaded [here](https://opig.stats.ox.ac.uk/webapps/newsabdab/sabdab/archive/all/). Extract `all_structures.zip` into the `data` folder. The `data` folder contains a snapshot of the dataset index (`sabdab_summary_all.tsv`).

We adopt [[DiffAb]](https://github.com/luost26/diffab) as the pretrained model and their weights can be downloaded from either [[Hugging Face]](https://huggingface.co/luost26/DiffAb/tree/main) or [[Google Drive]](https://drive.google.com/drive/folders/15ANqouWRTG2UmQS_p0ErSsrKsU4HmNQc?usp=sharing). Copy the files into the `trained_models` folder. 

### Configuration

The config files are in the `configs/test` folder. To design the six CDRs separately, use the `codesign_single` model and config on the scripts `design_pdb.py` (one sample) and `design_testset.py` (full test set, 19 samples). The lists of options are in the scripts [`diffab/tools/runner/design_for_pdb.py`](diffab/tools/runner/design_for_pdb.py) and [`diffab/tools/runner/design_for_testset.py`](diffab/tools/runner/design_for_testset.py), respectively.

For sampling by property (ddG, hydropathy, or both), use the following config files:

| Config file              | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| `codesign_single_ddg.yml` | Sequence-structure of one CDR, **sampling by ddG**. |
| `codesign_single_hydro.yml` | Sequence-structure of one CDR, **sampling by hydropathy**. |
| `codesign_single_ddg_and_hydro.yml` | Sequence-structure of one CDR, **sampling by ddG and hydropathy**. |

## Acknowledgements

This repository builds upon [(Morcillo et al. 2024)](http://github.com/amelvim/antibody-diffusion-properties), [(Luo et al. 2022) [DiffAb]](https://github.com/luost26/diffab), and [(Shan et al. 2022) [DDG Predictor]](https://github.com/HeliXonProtein/binding-ddg-predictor). Thanks to their contribution. 

## References

If you find this repository useful in your research, please cite the following works.

```bibtex
@article{lead25,
  title={Generative Co-Design of Antibody Sequences and Structures via Black-Box Guidance in a Shared Latent Space},
  author={Yinghua Yao, Yuangang Pan and Xixian Chen},
  journal={IJCAI},
  year={2025}
}
```
