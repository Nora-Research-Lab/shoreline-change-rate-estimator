![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Shoreline Change Rate Estimator
 
*For coastal scientists and geomorphologists: upload shoreline position dates and distances to get end-point and linear-regression shoreline change rates with a trend plot.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Coastal & Sedimentary Studies
 
This tool estimates shoreline change rates from repeated shore-normal position measurements. The user uploads a CSV file with two required columns: date (YYYY-MM-DD) and position_m (numeric, metres relative to a fixed baseline). A radio input selects the convention: seaward positive or landward positive. If landward positive is selected, all position values are multiplied by -1 before analysis. The tool parses the CSV, rejects missing or non-numeric values, sorts records by date ascending, and requires at least two valid rows. Dates are converted to decimal years using year plus day-of-year divided by 365.25. Two rates are calculated. The end-point rate is (last position - first position) divided by (last decimal year - first decimal year). The linear regression rate uses ordinary least squares: slope b = sum((t_i - t_mean)*(y_i - y_mean)) / sum((t_i - t_mean)^2), intercept a = y_mean - b*t_mean, and R² = 1 - SS_residual / SS_total. The standard error of the slope and a 95% confidence interval are computed using the Student t distribution with n-2 degrees of freedom. The Gradio interface shows the file upload and convention radio on the left and results on the right. Outputs are a parsed positions table, a Matplotlib scatter plot of position versus decimal year with the regression line, and a summary text block displaying the end-point rate, linear regression rate, R², 95% confidence interval, number of points, and date range. No AI component is used; the logic is ordinary least squares regression.
 
## Run it
 
```bash
docker build -t shoreline-change-rate-estimator .
docker run -p 7860:7860 shoreline-change-rate-estimator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-18.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
