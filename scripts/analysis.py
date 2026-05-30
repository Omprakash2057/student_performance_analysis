"""
Student Performance Analysis – Charts Generator
Produces 4 publication-quality charts saved to /report/charts/
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import os, warnings
warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(script_dir)
df   = pd.read_csv(os.path.join(BASE, 'data', 'student_records.csv'))
OUT  = os.path.join(BASE, 'report', 'charts')
os.makedirs(OUT, exist_ok=True)

# ── Palette ────────────────────────────────────────────────────────────────
C = {'High': '#2563EB', 'Medium': '#F59E0B', 'Low': '#EF4444'}
TIER_ORDER = ['High', 'Medium', 'Low']
BG  = '#F8FAFC'
GRID= '#E2E8F0'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': BG,
    'axes.facecolor': BG,
    'axes.grid': True,
    'grid.color': GRID,
    'grid.linewidth': 0.8,
})

# ── Chart 1: Average Subject Scores by Performance Tier ───────────────────
subjects = ['math_score', 'science_score', 'english_score', 'history_score']
labels   = ['Math', 'Science', 'English', 'History']

fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(subjects))
w = 0.26

for i, tier in enumerate(TIER_ORDER):
    vals = [df[df.performance_tier == tier][s].mean() for s in subjects]
    bars = ax.bar(x + (i-1)*w, vals, w, color=C[tier], label=tier,
                  zorder=3, linewidth=0)
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.6,
                f'{v:.1f}', ha='center', va='bottom', fontsize=8.5,
                fontweight='bold', color=C[tier])

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.set_ylabel('Average Score', fontsize=11)
ax.set_ylim(0, 105)
ax.set_title('Average Subject Scores by Performance Tier', fontsize=14,
             fontweight='bold', pad=14)
ax.legend(title='Tier', fontsize=10, title_fontsize=10, framealpha=0)
fig.tight_layout()
fig.savefig(f'{OUT}/01_subject_scores_by_tier.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 1 saved')

# ── Chart 2: Attendance vs Overall Score (line – binned) ──────────────────
df['att_bin'] = pd.cut(df.attendance_pct, bins=range(20, 105, 5),
                        labels=[f'{b}–{b+5}' for b in range(20, 100, 5)])
att_trend = df.groupby(['att_bin', 'performance_tier'], observed=True)['overall_score'].mean().reset_index()

fig, ax = plt.subplots(figsize=(11, 5.5))
for tier in TIER_ORDER:
    sub = att_trend[att_trend.performance_tier == tier].copy()
    ax.plot(sub['att_bin'].astype(str), sub['overall_score'],
            marker='o', markersize=5, linewidth=2.2, color=C[tier], label=tier, zorder=3)

ax.set_xlabel('Attendance Range (%)', fontsize=11)
ax.set_ylabel('Avg Overall Score', fontsize=11)
ax.set_title('Attendance vs Overall Score – Trend by Tier', fontsize=14,
             fontweight='bold', pad=14)
ax.tick_params(axis='x', rotation=45, labelsize=8.5)
ax.legend(title='Tier', fontsize=10, title_fontsize=10, framealpha=0)
fig.tight_layout()
fig.savefig(f'{OUT}/02_attendance_vs_score.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 2 saved')

# ── Chart 3: Study Hours Distribution (bar chart – binned) ────────────────
df['study_bin'] = pd.cut(df.study_hours_per_day,
                          bins=[0,1,2,3,4,5,6,7,8,10],
                          labels=['0–1','1–2','2–3','3–4','4–5','5–6','6–7','7–8','8+'])
study_grp = df.groupby(['study_bin','performance_tier'], observed=True).size().reset_index(name='count')

fig, ax = plt.subplots(figsize=(10, 5.5))
bins_u = study_grp['study_bin'].unique()
x = np.arange(len(bins_u))

for i, tier in enumerate(TIER_ORDER):
    sub = study_grp[study_grp.performance_tier == tier].set_index('study_bin')['count']
    vals = [sub.get(b, 0) for b in bins_u]
    ax.bar(x + (i-1)*0.26, vals, 0.26, color=C[tier], label=tier, zorder=3)

ax.set_xticks(x)
ax.set_xticklabels(bins_u, fontsize=10)
ax.set_xlabel('Study Hours per Day', fontsize=11)
ax.set_ylabel('Number of Students', fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'{int(v):,}'))
ax.set_title('Study Hours Distribution by Performance Tier', fontsize=14,
             fontweight='bold', pad=14)
ax.legend(title='Tier', fontsize=10, title_fontsize=10, framealpha=0)
fig.tight_layout()
fig.savefig(f'{OUT}/03_study_hours_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 3 saved')

# ── Chart 4: Key Metrics Summary – Horizontal Bar Comparison ─────────────
metrics = {
    'Avg Attendance (%)':         df.groupby('performance_tier')['attendance_pct'].mean(),
    'Avg Study Hours/Day':        df.groupby('performance_tier')['study_hours_per_day'].mean(),
    'Avg Overall Score':          df.groupby('performance_tier')['overall_score'].mean(),
}

fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
fig.suptitle('Key Metrics Comparison Across Performance Tiers',
             fontsize=14, fontweight='bold', y=1.01)

for ax, (title, series) in zip(axes, metrics.items()):
    vals  = [series[t] for t in TIER_ORDER]
    bars  = ax.barh(TIER_ORDER, vals, color=[C[t] for t in TIER_ORDER],
                    height=0.5, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(v + max(vals)*0.01, b.get_y()+b.get_height()/2,
                f'{v:.1f}', va='center', fontsize=10, fontweight='bold')
    ax.set_xlim(0, max(vals)*1.18)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8)
    ax.tick_params(axis='y', labelsize=11)
    ax.set_xlabel('')
    ax.spines['bottom'].set_visible(False)
    ax.xaxis.set_visible(False)

fig.tight_layout()
fig.savefig(f'{OUT}/04_key_metrics_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 4 saved')

# ── Print summary stats for report ────────────────────────────────────────
print('\n=== SUMMARY STATS ===')
print(df.groupby('performance_tier')[
    ['attendance_pct','study_hours_per_day','overall_score',
     'math_score','science_score','english_score','history_score']
].mean().round(2).to_string())
print(f'\nTotal records: {len(df):,}')
print(df['performance_tier'].value_counts())
