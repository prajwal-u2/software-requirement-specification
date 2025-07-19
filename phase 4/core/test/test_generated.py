import pytest
import pandas as pd
from core.py.scheduler import Scheduler

def test_generated():
	case = "generated"
	scheduler = Scheduler()
	scheduler.run(case)
	
	df = pd.read_csv(f"./data/{case}/schedule.csv")
	assert len(df) >= 800
