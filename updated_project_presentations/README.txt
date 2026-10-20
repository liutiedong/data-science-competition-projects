PROJECT PRESENTATIONS

The nine decks use the executed results in run_results/. Each deck contains a
main presentation followed by detailed results, remaining notebook figures,
model settings and questions for discussion.

powerpoints/              Editable PowerPoint decks
figures/notebook/         All 103 complete figures extracted from notebook outputs
figures/panels/           29 enlarged model panels
figures/<project>/       Comparisons and diagnostics generated from saved predictions
evidence/                Measured metrics, predictions and supplementary calculations
slide_image_map.csv/json Maps each slide image to its file and source cell or script
plot_coverage.csv/json   Coverage of every complete notebook figure
presenter_guide.txt       Main presentation and appendix slide ranges
code/                    Plot export, analysis and image-replacement utilities

Plots are PNG images embedded in the decks. Numerical tables and narrative text
remain editable. Notebook figures match the executed notebook outputs exactly.
The comparison figures show the best observed test configuration in each family
and the strongest penalized linear model. Complete tables retain every fitted
configuration, including equal-score configurations and stacking.

To refresh the original plots after running the notebooks:
  python code/export_notebook_figures.py --notebook-dir /path/to/project
To regenerate enlarged model panels without model fitting:
  python code/export_detail_panels.py --notebook-dir /path/to/project
Supplementary plots read evidence/<project>_results.json:
  python code/analyze_holdout.py
  python code/render_comparisons.py
If model winners change, rerun the analyses and revise the corresponding text,
metrics, model choices and captions. Image replacement alone does not update text.

To replace images in copies of the decks, using the image map:
  python code/replace_pptx_figures.py --output-dir /path/to/new_powerpoints
Keep the embedded-image hashes until replacement has completed. The utility
preserves slide layout and writes to a new directory.

Wine classification: the L1 and Elastic Net logistic fits reached 8,000
iterations without convergence. The deck identifies these scores as provisional.
The mock practice notebook and all dataset files remain outside this bundle.
