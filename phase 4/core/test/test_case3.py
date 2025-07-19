import pytest
import pandas as pd
from core.py.scheduler import Scheduler

def test_case3():
	case = "case3"
	scheduler = Scheduler()
	scheduler.run(case)
	
	df = pd.read_csv(f"./data/{case}/schedule.csv")
	assert len(df) == 64
