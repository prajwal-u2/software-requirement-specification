import pytest
import pandas as pd
from core.py.scheduler import Scheduler

def test_case4():
	case = "case4"
	scheduler = Scheduler()
	scheduler.run(case)
	
	df = pd.read_csv(f"./data/{case}/schedule.csv")
	assert len(df) == 96
