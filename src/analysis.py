
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.signal import find_peaks
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

INPUT_PATH = Path('data/processed/covid_deaths_enriched.csv')
SUMMARY_PATH = Path('data/processed/country_summary.csv')

def summarize_country(g: pd.DataFrame) -> pd.Series:
    g = g.sort_values('Day').reset_index(drop=True)
    peak_idx = g['rolling_7d'].idxmax()
    peak_value = float(g.loc[peak_idx, 'rolling_7d'])
    peak_date = pd.Timestamp(g.loc[peak_idx, 'Day'])
    peaks, _ = find_peaks(g['rolling_7d'].values, prominence=max(peak_value * 0.08, 0.15), distance=45)
    post = g[g['Day'] >= peak_date]
    recovery_match = post[post['rolling_7d'] <= peak_value * 0.25]
    recovery_days = int((recovery_match.iloc[0]['Day'] - peak_date).days) if not recovery_match.empty else np.nan
    return pd.Series({
        'peak_7d_deaths_per_million': peak_value,
        'peak_date': peak_date.date().isoformat(),
        'cumulative_deaths_per_million': float(g['deaths_per_million'].sum()),
        'avg_daily_deaths_per_million': float(g['deaths_per_million'].mean()),
        'volatility_std': float(g['deaths_per_million'].std()),
        'estimated_wave_count': int(len(peaks)),
        'days_to_recover_from_main_peak': recovery_days,
        'zero_share': float((g['deaths_per_million'] == 0).mean())
    })

def build_summary(input_path: Path = INPUT_PATH, output_path: Path = SUMMARY_PATH) -> pd.DataFrame:
    df = pd.read_csv(input_path, parse_dates=['Day'])
    summary = df.groupby('Entity', group_keys=False).apply(summarize_country).reset_index()
    feature_cols = [
        'peak_7d_deaths_per_million',
        'cumulative_deaths_per_million',
        'volatility_std',
        'estimated_wave_count',
        'days_to_recover_from_main_peak',
        'zero_share'
    ]
    X = StandardScaler().fit_transform(summary[feature_cols])
    km = KMeans(n_clusters=3, n_init=20, random_state=42)
    summary['cluster'] = km.fit_predict(X)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)
    return summary

if __name__ == '__main__':
    summary = build_summary()
    print(summary.sort_values('cumulative_deaths_per_million', ascending=False).to_string(index=False))
