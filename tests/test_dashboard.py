import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from build_dashboard import validate,summaries
def test_summary():
    df=validate(pd.read_csv(Path(__file__).parents[1]/"data/sample_program_data.csv"))
    s=summaries(df)
    assert len(s)==5 and s["Total Funding by Impact Area"].sum()==61000

