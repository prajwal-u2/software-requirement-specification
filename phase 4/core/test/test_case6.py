import pytest
import pandas as pd
from core.py.scheduler import Scheduler

def test_case6():
	case = "case6"
	scheduler = Scheduler()
	scheduler.run(case)
	
	df = pd.read_csv(f"./data/{case}/schedule.csv")
	assert len(df) >= 136
