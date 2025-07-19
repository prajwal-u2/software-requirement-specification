#include <iostream>
#include <string>

class Game {
public:
    int team1_id;
    int team2_id;
    int week;
    int day;
    std::string season;
    double start;
    double end;
    int venue_id;

    /**
     * Constructor to initialize a game object.
     * 
     * @param team1_id The ID of the first team.
     * @param team2_id The ID of the second team.
     * @param week The week of the season.
     * @param day The day of the week.
     * @param season The season (e.g., "2023").
     * @param start The start time of the game.
     * @param end The end time of the game.
     * @param venue_id The ID of the venue where the game is held.
     */
    Game(int team1_id, int team2_id, int week, int day, const std::string& season, double start, double end, int venue_id) 
        : team1_id(team1_id), team2_id(team2_id), week(week), day(day), season(season), start(start), end(end), venue_id(venue_id) {}

    /**
     * Prints a description of the game, including the teams, start and end times, week, and day.
     */
    void dump() const {
        std::cout << "Team " << team1_id << " vs. Team " << team2_id 
                  << " (" << start << "-" << end << ") Week: " << week 
                  << ", Day: " << day << ", Season: " << season << std::endl;
    }
};