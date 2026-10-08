import json
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="FraudScope — Layer 1", page_icon="🛡️", layout="wide")
st.title("🛡️ FraudScope — Transaction Detection Engine")
st.caption("Layer 1: transaction risk, operational thresholds and explainability foundation")

results_path = Path("reports/results.json")
comparison_path = Path("reports/model_comparison.csv")

if not comparison_path.exists():
    st.warning("No trained results found. Run: python -m fraudscope.cli train --data data/raw/creditcard.csv")
    st.stop()

comparison = pd.read_csv(comparison_path)
results = json.loads(results_path.read_text()) if results_path.exists() else {}

c1,c2,c3,c4 = st.columns(4)
best = comparison.sort_values("pr_auc", ascending=False).iloc[0]
c1.metric("Best PR-AUC", f"{best.pr_auc:.4f}")
c2.metric("Best Model", best.model)
c3.metric("Best Recall", f"{best.recall:.2%}")
c4.metric("Best F1", f"{best.f1:.4f}")

st.subheader("Model comparison")
st.dataframe(comparison, use_container_width=True)

st.subheader("Investigation capacity")
model = st.selectbox("Model", list(results.keys()))
if model in results:
    budget = pd.DataFrame(results[model]["capture_at_budget"])
    budget["alert_budget"] = budget["alert_budget"].map(lambda x: f"{x:.1%}")
    st.dataframe(budget, use_container_width=True)

st.subheader("Methodology")
st.markdown("""
- Chronological train/validation/test split
- Thresholds selected on validation data only
- PR-AUC prioritized because fraud is extremely imbalanced
- Test set remains untouched for final evaluation
- Behavioral features are only enabled when supported by actual dataset fields
""")
