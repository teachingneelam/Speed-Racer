import sqlite3

conn = sqlite3.connect("scores.db")
c = conn.cursor()

def create_table_scores():
    c.execute('''
            CREATE TABLE Scores(
                
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              score INTEGER NOT NULL,
              timer TEXT

                )
              
            ''')
    
def create_score(name, score, timer):
    with conn:
        c.execute("INSERT INTO Scores(name, score, timer) VALUES(:name, :score, :timer)", {"name":name, "score":score, "timer":timer})
        conn.commit()


def get_max_score():
    with conn:
        c.execute('SELECT score FROM Scores ORDER BY score DESC LIMIT 1')
        max_score = c.fetchone()[0]
    return max_score


def delete_lowest_score_if_exceeds_limit():
    with conn:
        c.execute("SELECT COUNT(*) FROM Scores")
        count = c.fetchone()[0]
        if count > 10:
            while count > 10:
                c.execute("DELETE FROM Scores WHERE id = (SELECT id FROM Scores ORDER BY score ASC, id ASC LIMIT 1)")
                conn.commit()
                c.execute("SELECT COUNT(*) FROM Scores")
                count = c.fetchone()[0]

def get_all_scores():
    with conn:
        c.execute("SELECT name, score, timer FROM Scores ORDER BY score DESC, id ASC")
        all_scores = c.fetchall()
    return all_scores

# Example usage
# create_table_scores()
# create_score("Alice", 95, "00:30:45")
# create_score("Bob", 87, "00:25:30")
# create_score("Charlie", 98, "00:27:15")
max_score = get_max_score()
print(max_score)
all_score = get_all_scores()
delete_lowest_score_if_exceeds_limit()
print((all_score))