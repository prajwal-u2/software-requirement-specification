import random
import os
from faker import Faker
import pandas as pd

def generate_season(min_weeks, start_week = 1, end_week = 52):
	min_weeks = min_weeks - 1 # Want exclusive, not inclusive
	start = random.randint(start_week, end_week)
	end = random.randint(start_week, end_week)
	if end < start:		
		t = end
		end = start
		start = t
	if end - start < min_weeks:
		overEnd = start + min_weeks
		overStart = end - min_weeks
		if overStart < start_week:
			start = start_week
			end = start + min_weeks
		elif overEnd > end_week:
			end = end_week
			start = end - min_weeks
		else:
			end = start + min_weeks
	return (int(start), int(end))	

# Assumes half hour slots in military time (0, 23.5)
def generate_availability(is_open=False):
	days = {}
	for i in range(1, 8):
		start = random.randint(0, 23) + random.randint(0, 1) / 2
		end = random.randint(0, 23) + random.randint(0, 1) / 2
		if end < start:
			t = start
			start = end
			end = t
		if is_open:
			days[f"d{i}Start"] = 0
			days[f"d{i}End"] = 23.5
		else:
			days[f"d{i}Start"] = start
			days[f"d{i}End"] = end
				
	return days

league_name = {
	1: "Platinum League",
	2: "Obsidian League",
	3: "Diamond League",
	4: "Ruby League",
	5: "Emerald League",
	6: "Sapphire League"
}

def generate_leagues(leagues = [(12, 20), (16, 16), (24, 12)]):
	leagueId = 1
	league_records = []
	for league in leagues:
		start = random.randint(12, 16)
		end = random.randint(20, 30)
		league_records.append({
			"leagueId": leagueId,
			"sportId": 4,
			"leagueTypeId": 1,
			"leagueName": f"{league_name[leagueId]}",
			"leagueSize": league[0],
			"seasonStart":start,
			"seasonEnd":end,
			"numberOfGames": league[1],
			"seasonYear":2024
		})
		leagueId += 1
	return league_records

team_nouns = [
	"Wolves", "Bulls", "Eagles", "Dolphins", "Wildcats", "Bobcats", "Bears", "Grizzlies", "Hornets",
	"Bucaneers", "Vikings", "Sox", "Chargers", "Warriors", "Sabres", "Americans", "Westerners", "Jacks",
	"Robbers", "Rappers", "Pirates", "Chiefs", "Commandos", "Celtics", "Mavericks", "Raptors", "Hawks"
]

def generate_teams(leagues = [(12, 20), (16, 16), (24, 12)]):
	faker = Faker()
	team_records = []
	teamId = 1
	leagueId = 1
	for league in leagues:
		for i in range(1, league[0] + 1):
			days = generate_availability(False)
			team_records.append({
				"teamId": teamId,
				"name": f"{faker.city()} {team_nouns[random.randint(1, len(team_nouns) - 1)]}",
				"leagueId": leagueId, # ids are 1..N not 0..N
				"sportId": 4, # ids are 1..N not 0..N
				"leagueTypeId": 1, # ids are 1..N not 0..N
				"players": 18,
				"region": "West",
				"d1Start": days["d1Start"],
				"d1End": days["d1End"],
				"d2Start": days["d2Start"],
				"d2End": days["d2End"],
				"d3Start": days["d3Start"],
				"d3End": days["d3End"],
				"d4Start": days["d4Start"],
				"d4End": days["d4End"],
				"d5Start": days["d5Start"],
				"d5End": days["d5End"],
				"d6Start": days["d6Start"],
				"d6End": days["d6End"],
				"d7Start": days["d7Start"],
				"d7End": days["d7End"],
			})
			teamId += 1
		leagueId += 1
	return team_records

location = ["Center", "Pavilion", "Plaza", "Field", "Place", "Oasis",
	"Complex", "Stadium", "Arena", "Park", "Grounds", "Facility",
	"Hub", "Dome", "Venue", "Zone", "Rink", "Court", "Gymnasium"] # rink and court sport specific

def generate_venues(leagues = [(12, 20), (16, 16), (24, 12)], team_to_venue_factor = 4):
	teams = 0
	faker = Faker()
	for league in leagues:
		teams += league[1] / 2 * league[0]
	teams /= team_to_venue_factor
	num_venues = int(teams)
	min_venue_weeks = 30
	venue_records = []
	for i in range(1, num_venues + 1):
		days = generate_availability(True)
		num_fields = random.randint(1, 4)
		start, end = generate_season(min_venue_weeks)
		name = f"{faker.city()} {location[random.randint(0, len(location) - 1)]}"
		for k in range(1, num_fields):
			venue_records.append({
				"venueId": i + k - 1,
				"region": "West",
				"name": name,
				"field": k,
				"d1Start": days["d1Start"],
				"d1End": days["d1End"],
				"d2Start": days["d2Start"],
				"d2End": days["d2End"],
				"d3Start": days["d3Start"],
				"d3End": days["d3End"],
				"d4Start": days["d4Start"],
				"d4End": days["d4End"],
				"d5Start": days["d5Start"],
				"d5End": days["d5End"],
				"d6Start": days["d6Start"],
				"d6End": days["d6End"],
				"d7Start": days["d7Start"],
				"d7End": days["d7End"],
				"seasonStart": start,
				"seasonEnd": end,
				"seasonYear": "2024"
			})
	return venue_records

def generate(case="case6"):
	directory = f"./data/{case}/"	

	league_constraints = [(24, 14), (32, 24), (48, 20)]
	leagues = generate_leagues(league_constraints)
	teams = generate_teams(league_constraints)
	venues = generate_venues(league_constraints, 100)
	
	dfs = {
		"team": pd.DataFrame(teams),
		"league": pd.DataFrame(leagues),
		"venue": pd.DataFrame(venues),
	}
	
	os.makedirs(directory, exist_ok=True)
		
	for basename, frame in dfs.items():
		frame.to_csv(f"{directory}{basename}.csv", index=False)
		
if __name__ == "__main__":
	generate("case8")