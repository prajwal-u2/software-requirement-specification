class Game:
	def __init__(self, team1_name, team2_name, week, day, season, start, end, venue_name):
		self.team1_name = team1_name
		self.team2_name = team2_name
		self.week = week
		self.day = day
		self.season = season
		self.start = start
		self.end = end
		self.venue_name = venue_name
		
	def dump(self):
		print(f"Team {self.team1_name} vs. Team {self.team2_name} ({self.start}-{self.end}) {self.week} {self.day}")