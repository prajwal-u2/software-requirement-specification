import sys
import pandas as pd

class Scheduler:
	
	@staticmethod
	def run(case: str = "case1") -> int:
		"""
		Scheduling algorithm that takes in various data files to schedule games involving different sports, regions, and leagues.
		
		Return:
			int: Returns 0 if successful.
		"""
		
		input_teams: str = f"./data/{case}/team.csv"
		input_venues: str = f"./data/{case}/venue.csv"
		input_leagues: str = f"./data/{case}/league.csv"

		input_sports = {
			1: "Basketball",
			2: "Soccer",
			3: "Baseball",
			4: "Softball",
			5: "Kickball",
			6: "Dodgeball",
			7: "Hockey"
		}
		
		team_df = pd.DataFrame()
		venue_df = pd.DataFrame()
		league_df = pd.DataFrame()
		
		games = []
		
		schedule_records = []
		for game in games:
			game.dump()
			team1 = team_df[team_df["teamId"] == game.team1_id].to_dict(orient="records")
			team2 = team_df[team_df["teamId"] == game.team2_id].to_dict(orient="records")
			venue = venue_df[venue_df["venueId"] == game.venue_id].to_dict(orient="records")
			league = league_df[league_df["leagueId"] == team1[0]["leagueId"]].to_dict(orient="records")
			schedule_records.append({
				"team1Name": team1[0]["name"],
				"team2Name": team2[0]["name"],
				"week": game.week, 
				"day": game.day, 
				"start": game.start, 
				"end": game.end,
				"season": game.season,
				"league": league[0]["leagueName"],
				"location": f"{venue[0]["name"]} Field #{venue[0]["field"]}"
			})
			
		schedule_df = pd.DataFrame(schedule_records)
		schedule_df.to_csv(f"./data/{case}/schedule.csv", index=False)		
		schedule_df.to_json(f"./data/{case}/schedule.json")
		
		return 0
	
if __name__ == "__main__":
	case = sys.argv[1]	

	schedule = Scheduler()
	schedule.run(case)