ONLINE SHOPPING PURCHASE PREDICTION

online_shoppers_practice.ipynb is your working exercise notebook.
Keep your code and written interpretations there. Updating the worked solution does
not reset or execute the practice notebook.

online_shoppers_solution.ipynb is the executed reference. It uses plain pandas,
direct estimator.fit calls and short parameter loops. The only custom helper records
classification metrics; no fitting or prediction is hidden inside it.
Run the solution top to bottom from this directory using a Python environment with
requirements.txt installed. All data are local; no Kaggle account is needed to run it.

Files
online_shoppers_intention.csv    Unmodified public Kaggle data
online_shoppers_practice.ipynb   Your practice notebook
online_shoppers_solution.ipynb   Executed worked solution
requirements.txt                Reference package versions
data_dictionary.csv             Predictor and target definitions
dataset_source.json             Download URL, citation, license and checksum
outputs/                        Measured tables, predictions and 18 plot images

Task
Predict Revenue (purchase or no purchase) from session summaries.
Select a model by validation average precision (AP) and a cutoff by validation F1.
Compare logistic regression, L2/L1/Elastic Net logistic models, KNN, MLP,
Random Forest, XGBoost, CatBoost and LightGBM. Evaluate a fixed three-model stack.

Workflow
Objective; setup; inspection; splitting; training-only EDA; feature engineering;
encoding and scaling; individual models; short tuning loops; comparison; stacking;
feature ablation; cutoff selection; final test; interpretation and error analysis;
capacity and uncertainty; conclusion; presentation Q&A.

Preparation and evaluation
The solution removes 125 exact duplicate records, leaving 12,205 distinct records.
There are then no repeated predictor profiles. A stratified random split allocates
60% to training, 20% to validation and 20% to test. This evaluates distinct recorded
profiles; repeated summaries could have represented distinct real sessions.

One-hot columns come from training categories. Validation and test are aligned to
those columns. StandardScaler is fitted only on training inputs. CatBoost uses the
same one-hot inputs as the other tree models to keep the workflow straightforward.

Each linear penalty tries three C values. Each nonlinear tuning loop tries two values
of one parameter. All candidates use the training partition; MLP keeps an internal
early-stopping holdout. These are validation searches, not cross-validation searches.
The stack alone uses three-fold out-of-fold training probabilities for its meta-model.

The explicit final model assignment follows the validation AP ranking. If you change
features or model settings, check the new ranking and update that assignment before
continuing. The cutoff is selected on validation data. The estimator is kept unchanged
for the final test so the cutoff stays attached to the same fitted probability model.
Ablations are fixed-configuration diagnostics, separate from the main model ranking.

The final analysis includes probability calibration, confusion matrices, encoded-column
permutation importance, group errors, capacity curves and conditional bootstrap intervals.
Session summaries may be unavailable at an early intervention time. The data have no
visitor IDs or full timestamps, so visitor independence and future transfer are untested.
Purchase propensity should not be interpreted as incremental marketing response.

Outputs
validation_results.csv and validation_predictions.csv contain every main model.
validation_cutoffs.csv records the cutoff grid. test_results.csv and test_predictions.csv
record the final held-out evaluation. Other CSVs contain splits, ablation, importance,
group performance, capacity and bootstrap intervals. Every notebook plot is saved
under outputs/figures and can be replaced directly after another run.

Sources
Kaggle: https://www.kaggle.com/datasets/henrysue/online-shoppers-intention
Original: https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset
Citation: Sakar, C. & Kastro, Y. (2018). Online Shoppers Purchasing Intention Dataset.
UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5F88Q.
Original dataset license: Creative Commons Attribution 4.0.
