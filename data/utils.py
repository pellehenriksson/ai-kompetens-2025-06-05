# create file of masters winners

import pandas as pd
import re

def clean(s: str) -> str:
    return re.sub(r"\s*\([^)]*\)", "", s)

df = pd.read_html("https://sv.wikipedia.org/wiki/The_Masters_Tournament")[1]
df.columns = ["year", "winner", "country", "score", "margin"]

df["winner"] = df["winner"].apply(clean)

df.to_csv("data/masters-winners.csv", columns=["year", "winner", "country"], index=False)