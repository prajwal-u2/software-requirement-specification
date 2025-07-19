from faker import Faker
import random
import pandas as pd
import math
import os
from core.py.interval_tree import IntervalTree, Interval

if __name__ == "__main__":

	def generate(directory):

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
		def generate_availability():
			days = {}
			for i in range(1, 8):
				start = random.randint(0, 23) + random.randint(0, 1) / 2
				end = random.randint(0, 23) + random.randint(0, 1) / 2
				if end < start:
					t = start
					start = end
					end = t
				days[f"d{i}Start"] = start
				days[f"d{i}End"] = end
						
			return days
		
		faker = Faker()
		
		league_type = ["Recreational", "Junior", "Competitive"]
		
		sports = ["Basketball", "Soccer", "Baseball", "Softball", "Kickball", "Dodgeball", "Hockey"]

		team_to_venue_factor = 5
		num_teams = (len(sports) * 100)
		num_venues = int(num_teams / team_to_venue_factor)
		season_year = 2024

		league_minimum = num_teams / (len(sports)) # 500

		team_nouns = [
			"Wolves", "Bulls", "Eagles", "Dolphins", "Wildcats", "Bobcats", "Bears", "Grizzlies", "Hornets",
			"Bucaneers", "Vikings", "Sox", "Chargers", "Warriors", "Sabres", "Americans", "Westerners", "Jacks",
			"Robbers", "Rappers", "Pirates", "Chiefs", "Commandos", "Celtics", "Mavericks", "Raptors", "Hawks"
		]
		
		regions = [
			"West",
			"North",
			"East",
			"South",
			"Central"	
		]

		max_player_limits = {
			"Basketball": [100, 10, 10],
			"Soccer": [100, 10, 10],
			"Baseball": [100, 10, 26],
			"Softball": [100, 10, 10],
			"Kickball": [100, 10, 10],
			"Dodgeball": [100, 10, 10],
			"Hockey": [100, 10, 10],
		}
		
		min_game_limits = {
			"Basketball": [32, 32, 32],
			"Soccer":  [32, 32, 32],
			"Baseball":  [32, 32, 32],
			"Softball":  [32, 32, 32],
			"Kickball":  [32, 32, 32],
			"Dodgeball":  [32, 32, 32],
			"Hockey":  [32, 32, 32],
		}
		
		min_player_limits = {
			"Basketball": 5,
			"Soccer": 10,
			"Baseball": 10,
			"Softball": 10,
			"Kickball": 10,
			"Dodgeball": 10,
			"Hockey": 10,
		}
		
		# Assuming two leagues will have min and max of 16 games
		# Recreational has not restrictions
		num_teams = {
			"Basketball": [1000, 16, 16],
			"Soccer":  [1000, 16, 16],
			"Baseball":  [1000, 16, 16],
			"Softball":  [1000, 16, 16],
			"Kickball":  [1000, 16, 16],
			"Dodgeball":  [1000, 16, 16],
			"Hockey":  [1000, 16, 16],
		}
		
		# Synthetic Sports and Leagues
		
		sport_records = []
		league_records = []
		
		league_to_sport_map = {}
		
		leagueId = 1
		for i in range(1, len(sports) + 1):
			sport_records.append({
				"sportId": i,
				"sport": sports[i - 1]	
			})
			for j in range(1, len(league_type) + 1):
				start = random.randint(1, 52)
				end = random.randint(1, 52)
				league_to_sport_map[j] = i
				start, end = generate_season(min_game_limits[sports[i - 1]][j - 1] / 2) # Minimum 2 games a week
				league_records.append({
					"leagueId": leagueId,
					"sportId": i,
					"leagueTypeId": j,
					"leagueName": league_type[j - 1],
					"leagueSize": num_teams[sports[i - 1]][j - 1],
					"seasonStart":start,
					"seasonEnd":end,
					"numberOfGames": min_game_limits[sports[i - 1]][j - 1],
					"seasonYear":season_year
				})
				leagueId += 1

		# Synthetic Teams and Players

		team_records = []
		player_records = []

		teamId = 1
		playerId = 1
		for sportId in range(len(sports)):
			tiers = num_teams[sports[sportId]]
			tiers.reverse()
			any_tier = league_minimum # May need a sanity check to make sure all leagues viable, i.e. what if value is less than 16 * 3
			for t in tiers[:-1]:
				any_tier -= t
			tiers[len(tiers) - 1] = math.ceil(any_tier)
			print(tiers)
			
			for n in range(len(tiers)):
				
				league_type_id = (len(league_type) - 1 - n)

				num_teams_for_league = int(tiers[n])
				
				# Ensure number of teams is even
				if num_teams_for_league % 2 != 0:
					num_teams_for_league += 1

				print(num_teams_for_league)
				for i in range(1, num_teams_for_league + 1):
					
					minLim = min_player_limits[sports[sportId]]
					maxLim = max_player_limits[sports[sportId]][league_type_id]
					
					leagueId = (sportId + 1) * 3 + (league_type_id + 1) # See first loop for intrinsic relationship between sport, league_type and league_id
					
					num_players = random.randint(minLim, maxLim)
					for j in range(1, num_players + 1):
						free_agent = 999
						if maxLim - minLim > 2:
							free_agent = random.randint(1, 100)
								
						# Ensures minimum amount of players available with 25% for free agent
						# if any overage
						teamIdCopy = teamId
						if free_agent < 25 and num_players > minLim:
							teamIdCopy = None
							num_players -= 1
						player_records.append({
							"playerId": playerId,
							"name": f"{faker.first_name_male()} {faker.last_name()}",
							"email": f"{faker.email()}",
							"teamId": f"{teamIdCopy}",
							"sportId": sportId,
							"leagueId": leagueId
						})
						playerId += 1
						
					days = generate_availability()
					region = regions[random.randint(0, 4)]
					
					rand = random.randint(0, len(team_nouns) - 1)

					team_records.append({
						"teamId": teamId,
						"name": f"{faker.city()} {team_nouns[rand]}",
						"leagueId": leagueId + 1, # ids are 1..N not 0..N
						"sportId": sportId + 1, # ids are 1..N not 0..N
						"leagueTypeId": league_type_id + 1, # ids are 1..N not 0..N
						"players": num_players,
						"region": region,
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

		# Synthetic Venues

		venue_records = []
		min_venue_weeks = 20
		location = ["Center", "Pavilion", "Plaza", "Field", "Place", "Oasis",
				"Complex", "Stadium", "Arena", "Park", "Grounds", "Facility",
				"Hub", "Dome", "Venue", "Zone", "Rink", "Court", "Gymnasium"] # rink and court sport specific
		for i in range(1, num_venues + 1):
			days = generate_availability()
			region = regions[random.randint(0, 4)]
			num_fields = random.randint(1, 6)
			start, end = generate_season(min_venue_weeks)
			name = f"{faker.city()} {location[random.randint(0, len(location) - 1)]}"
			for k in range(1, num_fields):
				venue_records.append({
					"venueId": i + k - 1,
					"region": region,
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
					"seasonYear": season_year
				})

		dfs = {
			"team": pd.DataFrame(team_records),
			"player": pd.DataFrame(player_records),
			"league": pd.DataFrame(league_records),
			"venue": pd.DataFrame(venue_records),
			"sport": pd.DataFrame(sport_records)
		}
		
		for basename, frame in dfs.items():
			frame.to_csv(f"{directory}{basename}.csv", index=False) 
	
	def load_frames(directory):
		frames = {}
		files = os.listdir(directory)
		for f in files:
			df = pd.read_csv(directory + f)
			base = f.split(".")[0]
			frames[base] = df
		return frames
	
	directory = "./data/generated/"
		
	generate(directory)
		
	dfs = load_frames(directory)