from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt

REQUIRED={"program_id","department","partnership_type","impact_area","satisfaction","funding","student_volunteers"}
def validate(df):
    missing=REQUIRED-set(df.columns)
    if missing: raise ValueError(f"Missing columns: {sorted(missing)}")
    if df["program_id"].duplicated().any(): raise ValueError("Duplicate program_id")
    if not df["satisfaction"].between(1,5).all(): raise ValueError("Satisfaction outside 1-5")
    if (df[["funding","student_volunteers"]]<0).any().any(): raise ValueError("Negative funding/volunteers")
    return df
def summaries(df):
    return {
      "Participants by Department":df.groupby("department").size(),
      "Partnerships by Type":df.groupby("partnership_type").size(),
      "Average Satisfaction by Impact Area":df.groupby("impact_area")["satisfaction"].mean(),
      "Total Funding by Impact Area":df.groupby("impact_area")["funding"].sum(),
      "Student Volunteers by Impact Area":df.groupby("impact_area")["student_volunteers"].sum()}
def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); a=p.parse_args()
    root=Path(__file__).parents[1]; out=root/"outputs"; out.mkdir(exist_ok=True)
    df=validate(pd.read_csv(a.input)); s=summaries(df)
    with pd.ExcelWriter(out/"stakeholder_summary.xlsx") as w:
        for name,v in s.items(): v.rename("value").to_excel(w,sheet_name=name[:31])
    fig,axs=plt.subplots(2,3,figsize=(14,8));
    for ax,(title,v) in zip(axs.flat,s.items()): v.sort_values().plot.barh(ax=ax,title=title); ax.set_ylabel("")
    axs.flat[-1].axis("off"); fig.suptitle("Program Engagement Dashboard",fontsize=18,fontweight="bold")
    plt.tight_layout(); plt.savefig(out/"program_dashboard.png",dpi=160); plt.close()
if __name__=="__main__": main()

