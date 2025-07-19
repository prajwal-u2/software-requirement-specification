package core.java.src;

public class Game {
	private int team1_id;
	private int team2_id;
	private int week;
	private int day;
	private String season;
	private double start;
	private double end;
	private int venue_id;

	/**
	 * Constructor to initialize a game object.
	 * 
	 * @param team1_id The ID of the first team.
	 * @param team2_id The ID of the second team.
	 * @param week     The week of the season.
	 * @param day      The day of the week.
	 * @param season   The season (e.g., "2023").
	 * @param start    The start time of the game.
	 * @param end      The end time of the game.
	 * @param venue_id The ID of the venue where the game is held.
	 */
	public Game(int team1_id, int team2_id, int week, int day, String season, double start, double end, int venue_id) {
		this.team1_id = team1_id;
		this.team2_id = team2_id;
		this.week = week;
		this.day = day;
		this.season = season;
		this.start = start;
		this.end = end;
<<<<<<< HEAD
		this.venue_id = venue_id;
=======
		this.venueName = venueName;
>>>>>>> 1753de3e1b880f70d6396ef2fc25c8efe9bd17dc
	}

	/**
     * Prints a description of the game, including the teams, start and end times, week, and day.
     */
    public void dump() {
<<<<<<< HEAD
        System.out.println("Team " + team1_id + " vs. Team " + team2_id + 
=======
        System.out.println("Team " + team1Name + " vs. Team " + team2Name + 
>>>>>>> 1753de3e1b880f70d6396ef2fc25c8efe9bd17dc
                           " (" + start + "-" + end + ") Week: " + week + 
                           ", Day: " + day + ", Season: " + season);
    }
}