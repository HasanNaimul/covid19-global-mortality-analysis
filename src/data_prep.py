
import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = Path('data/raw/daily-new-confirmed-covid-19-deaths-per-million-people.csv')
OUTPUT_PATH = Path('data/processed/covid_deaths_enriched.csv')

def build_dataset(input_path: Path = RAW_PATH, output_path: Path = OUTPUT_PATH) -> pd.DataFrame:
    df = pd.read_csv(input_path, parse_dates=['Day']).rename(columns={'New deaths (per 1M)': 'deaths_per_million'})
    df = df.sort_values(['Entity', 'Day']).reset_index(drop=True)
    df['rolling_7d'] = df.groupby('Entity')['deaths_per_million'].transform(lambda s: s.rolling(7, min_periods=1).mean())
    df['year'] = df['Day'].dt.year
    df['month'] = df['Day'].dt.to_period('M').astype(str)
    df['quarter'] = df['Day'].dt.to_period('Q').astype(str)
    df['is_weekend'] = df['Day'].dt.dayofweek >= 5
    df['daily_change'] = df.groupby('Entity')['deaths_per_million'].diff()
    df['pct_change'] = df.groupby('Entity')['deaths_per_million'].pct_change().replace([np.inf, -np.inf], np.nan)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df

if __name__ == '__main__':
    result = build_dataset()
    print(f'Saved enriched dataset with {len(result):,} rows to {OUTPUT_PATH}')
