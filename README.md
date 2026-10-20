# Data Science Competition Projects

Worked machine-learning projects, practice notebooks, datasets, measured results and final PowerPoint presentations. The collection covers tabular regression, classification and time-series forecasting.

The notebooks contain saved outputs. The presentations explain the objectives, data preparation, exploratory analysis, models, results and limitations. Their plots are embedded images, with the source PNG files included for replacement after a new run.

## Projects

| Project | Notebook | Final presentation |
| --- | --- | --- |
| California housing | [Regression models](ml_models_tutorial.ipynb) | [PowerPoint](updated_project_presentations/powerpoints/01_california_housing_REVISED.pptx) |
| Wine quality | [Regression and classification](wine_quality_tutorial.ipynb) | [PowerPoint](updated_project_presentations/powerpoints/02_wine_quality_REVISED.pptx) |
| Sailing boat prices | [Price prediction](sailing_boats_tutorial.ipynb) | [PowerPoint](updated_project_presentations/powerpoints/03_sailing_boats_REVISED.pptx) |
| Cryptocurrency microstructure | [Market data analysis](crypto_microstructure_tutorial.ipynb) | [PowerPoint](updated_project_presentations/powerpoints/04_crypto_microstructure_REVISED.pptx) |
| PJM energy | [Electricity forecasting](pjm_energy_tutorial.ipynb) | [PowerPoint](updated_project_presentations/powerpoints/05_pjm_energy_REVISED.pptx) |
| German electricity | [Power systems forecasting](open_power_systems_tutorial.ipynb) | [PowerPoint](updated_project_presentations/powerpoints/06_german_electricity_REVISED.pptx) |
| Give Me Some Credit | [Credit classification](give_me_some_credit_tutorial.ipynb) | [PowerPoint](updated_project_presentations/powerpoints/07_give_me_some_credit_REVISED.pptx) |
| Home Credit | [Default prediction](home_credit_tutorial.ipynb) | [PowerPoint](updated_project_presentations/powerpoints/08_home_credit_REVISED.pptx) |
| American Express | [Default prediction](amex_default_tutorial.ipynb) | [PowerPoint](updated_project_presentations/powerpoints/09_amex_default_REVISED.pptx) |

## Mock assignments

| Assignment | Practice | Worked solution |
| --- | --- | --- |
| Online shopping purchases: classification | [Practice](mock/online_shoppers_practice.ipynb), [categorical-feature variant](mock/online_shoppers_practice_drop_cat.ipynb) | [Solution](mock/online_shoppers_solution.ipynb) |
| Medical insurance costs: regression | [Practice](mock/regression/medical_cost_practice.ipynb) | [Solution](mock/regression/medical_cost_solution.ipynb) |

Practice notebooks include the work saved at publication time. The worked mock solutions use direct estimator fits, straightforward pandas preparation and short tuning loops. Their READMEs explain the splits, selection metrics and evaluation procedures.

## Get started

Use Python 3.13 and Git LFS. Two datasets are stored in LFS because they exceed GitHub's ordinary Git file-size limit.

```bash
git lfs install
git clone https://github.com/liutiedong/data-science-competition-projects.git
cd data-science-competition-projects
git lfs pull

python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

On Windows, activate the environment with `.venv\Scripts\activate`.

Run the nine main notebooks from the repository root. Run each mock notebook from its own directory: `mock/` or `mock/regression/`. The housing and wine notebooks use scikit-learn dataset loaders and may need internet access on their first run. Other supplied datasets retain their existing relative paths. The sailing project reads the included Excel workbook.

## Repository contents

- Root notebooks and datasets: the nine main projects and their local input files.
- `crypto_microstructure_raw/`: source cryptocurrency CSV files.
- `mock/`: classification practice, solution, dataset, data dictionary and saved analysis.
- `mock/regression/`: regression practice, solution, dataset and saved analysis.
- `run_results/`: saved metrics, predictions, notebook figures and execution records for the main projects.
- `updated_project_presentations/powerpoints/`: the nine final editable PowerPoint decks.
- `updated_project_presentations/figures/`: notebook figures and supporting plot images.
- `updated_project_presentations/evidence/`: presentation metrics and supporting results.
- `updated_project_presentations/code/`: figure export, analysis and PowerPoint image-replacement utilities.

## Reading the results

Use each notebook's split and metric definitions when interpreting its tables. Regression, classification and forecasting scores are not directly interchangeable. Model rankings describe the recorded experiments, rather than universal performance claims.

The wine presentation identifies the L1 and Elastic Net logistic fits that reached their iteration limit as provisional. Other project-specific assumptions and limitations are documented in the notebooks and decks.

Changing data or settings requires rerunning the affected notebook and refreshing its result tables, plots and presentation text. The [presentation README](updated_project_presentations/README.txt) explains the figure export and image-replacement commands.

## Data sources

The notebooks document their input sources. The mock datasets include dedicated provenance files: [online shoppers](mock/dataset_source.json) and [medical insurance](mock/regression/dataset_source.json). American Express inputs are the supplied 1% sample; Home Credit includes the supplied application-training table.

Datasets retain their original licenses and usage terms. Consult the original sources before reuse; this repository does not replace those terms.
