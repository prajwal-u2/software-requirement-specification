import pytest
import pandas as pd
from core.py.scheduler import Scheduler

def test_case1():
	case = "case1"
	scheduler = Scheduler()
	scheduler.run(case)
	
	df = pd.read_csv(f"./data/{case}/schedule.csv")
	assert len(df) == 32
