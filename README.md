# Student Performance Analysis

## Project Overview
Analysed ~10,000 student records to understand how attendance, study hours, and subject scores relate to overall academic performance.

## Project Structure
```
student_performance_analysis/
├── data/
│   └── student_records.csv        # 10,000 student records
├── scripts/
│   ├── generate_data.py           # Dataset generation
│   ├── analysis.py                # Charts generation (Pandas + Matplotlib)
│   └── sql_analysis.py            # SQL-style groupby analysis
└── report/
    ├── Student_Performance_Report.html   # Main stakeholder report
    └── charts/
        ├── 01_subject_scores_by_tier.png
        ├── 02_attendance_vs_score.png
        ├── 03_study_hours_distribution.png
        └── 04_key_metrics_comparison.png
```

## Key Findings
| Metric            | High Tier | Medium Tier | Low Tier |
|-------------------|-----------|-------------|----------|
| Avg Attendance    | 90.1%     | 75.0%       | 57.6%    |
| Avg Study Hrs/Day | 6.5       | 4.0         | 2.1      |
| Avg Overall Score | 82.5      | 65.0        | 47.9     |

## Tools Used
- **Python** · Pandas, NumPy, Matplotlib, Seaborn
- **SQL-style analysis** via Pandas groupby aggregations
- **Report** as self-contained HTML with embedded charts

## Demo
![Student Performance Analysis Report](Recording%202026-05-30%20095959.gif)
