MEDICAL COST REGRESSION MOCK

Start with medical_cost_practice.ipynb and write your own code.
medical_cost_solution.ipynb is the executed reference solution.
The dataset is insurance.csv. Predict charges, a continuous target in US dollars.

Open the notebooks from this directory so the relative paths work.
Use a Python environment with the packages in requirements.txt.
No network access or Kaggle account is needed to run the notebooks.

The solution uses pandas, train_test_split, get_dummies, StandardScaler and
ordinary model.fit calls. One short evaluate function calculates metrics.
Each model has its own cell. Parameter searches are short loops over two values
(or three penalty strengths), with candidates compared on validation RMSE.
Models fit all training rows. StackingRegressor generates its own out-of-fold
predictions using three training folds. The chosen model refits on training plus
validation before final test evaluation.

The source CSV has 1,338 rows. The solution removes one exact duplicate from the
modeling frame, then makes a random train/validation/test split. It retains
records that share predictors but have different charges. Random splitting and
the absence of customer identifiers remain limitations.

Workflow: objective, data inspection, split, EDA, feature engineering,
preprocessing, baselines, OLS, Ridge, Lasso, Elastic Net, KNN, MLP, Random Forest,
XGBoost, CatBoost, LightGBM, tuning, comparison, stacking, feature ablation,
log target, final selection, test errors, permutation importance, bootstrap,
conclusion and presentation questions.

The practice prompts also cover group-aware cross-validation as an extension.
The reference uses short validation searches to keep its code straightforward.

Files
medical_cost_practice.ipynb   Practice prompts and your code cells
medical_cost_solution.ipynb   Executed reference solution
insurance.csv                Unmodified source CSV
data_dictionary.csv          Column definitions
dataset_source.json          Kaggle source, license and checksum
requirements.txt             Reference package versions
outputs/                     Current result tables, predictions and plot images

Kaggle: https://www.kaggle.com/datasets/mirichoi0218/insurance
