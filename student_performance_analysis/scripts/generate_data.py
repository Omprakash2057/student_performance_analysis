"""
Student Performance Dataset Generator
Generates ~10,000 realistic student records with attendance, study hours, and scores.
"""
import numpy as np
import pandas as pd

np.random.seed(42)
N = 10000

# Performance tiers
tiers = np.random.choice(['High', 'Medium', 'Low'], size=N, p=[0.25, 0.50, 0.25])

attendance = np.where(
    tiers == 'High', np.clip(np.random.normal(90, 5, N), 70, 100),
    np.where(tiers == 'Medium', np.clip(np.random.normal(75, 8, N), 50, 95),
             np.clip(np.random.normal(58, 10, N), 20, 80))
)

study_hours = np.where(
    tiers == 'High', np.clip(np.random.normal(6.5, 1.2, N), 3, 10),
    np.where(tiers == 'Medium', np.clip(np.random.normal(4.0, 1.5, N), 1, 8),
             np.clip(np.random.normal(2.0, 1.0, N), 0.5, 5))
)

def gen_scores(tier, subject_bias=0):
    base = {'High': 82, 'Medium': 65, 'Low': 48}[tier[0]] + subject_bias
    return np.clip(
        np.where(tier == 'High', np.random.normal(base, 7, N),
        np.where(tier == 'Medium', np.random.normal(base, 9, N),
                 np.random.normal(base, 8, N))), 0, 100
    ).round(1)

math    = gen_scores(tiers,  0)
science = gen_scores(tiers,  2)
english = gen_scores(tiers, -1)
history = gen_scores(tiers,  1)

overall = (math * 0.30 + science * 0.30 + english * 0.20 + history * 0.20).round(1)

df = pd.DataFrame({
    'student_id':    [f'STU{str(i).zfill(5)}' for i in range(1, N+1)],
    'gender':        np.random.choice(['Male', 'Female'], N, p=[0.50, 0.50]),
    'grade_level':   np.random.choice([9, 10, 11, 12], N),
    'attendance_pct': attendance.round(1),
    'study_hours_per_day': study_hours.round(1),
    'math_score':    math,
    'science_score': science,
    'english_score': english,
    'history_score': history,
    'overall_score': overall,
    'performance_tier': tiers
})

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
data_path = os.path.join(base_dir, 'data', 'student_records.csv')
df.to_csv(data_path, index=False)
print(f"Dataset created: {len(df):,} records")
print(df['performance_tier'].value_counts())
