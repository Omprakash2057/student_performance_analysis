"""
SQL-style Analysis using Pandas (mirrors what you'd run in a SQL DB)
"""
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
data_path = os.path.join(base_dir, 'data', 'student_records.csv')
df = pd.read_csv(data_path)

# Register as SQL table using pandasql
try:
    import pandasql as ps
    students = df
    q1 = """
    SELECT performance_tier,
           COUNT(*) as student_count,
           ROUND(AVG(attendance_pct), 2) as avg_attendance,
           ROUND(AVG(study_hours_per_day), 2) as avg_study_hours,
           ROUND(AVG(overall_score), 2) as avg_score
    FROM students
    GROUP BY performance_tier
    ORDER BY avg_score DESC
    """
    print("=== SQL Query Result ===")
    print(ps.sqldf(q1, locals()).to_string(index=False))
except ImportError:
    # Simulate SQL with Pandas groupby
    result = df.groupby('performance_tier').agg(
        student_count=('student_id','count'),
        avg_attendance=('attendance_pct','mean'),
        avg_study_hours=('study_hours_per_day','mean'),
        avg_score=('overall_score','mean')
    ).round(2).sort_values('avg_score', ascending=False)
    print("=== GROUP BY Performance Tier ===")
    print(result.to_string())

print("\n=== Attendance Quartile Analysis ===")
df['att_quartile'] = pd.qcut(df.attendance_pct, q=4, labels=['Q1 (Low)','Q2','Q3','Q4 (High)'])
print(df.groupby('att_quartile', observed=True)['overall_score'].mean().round(2))
