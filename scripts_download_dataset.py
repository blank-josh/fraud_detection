"""Download the ULB/Kaggle dataset using Kaggle CLI after authentication."""
from pathlib import Path
import subprocess, sys
root=Path(__file__).resolve().parent
raw=root/'data'/'raw'
raw.mkdir(parents=True, exist_ok=True)
cmd=[sys.executable,'-m','kaggle','datasets','download','-d','mlg-ulb/creditcardfraud','-p',str(raw),'--unzip']
print('Running:', ' '.join(cmd))
subprocess.check_call(cmd)
print('Expected file:', raw/'creditcard.csv')
