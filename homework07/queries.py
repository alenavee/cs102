import psycopg2
from tabulate import tabulate

# Function to run queries
def fetch_all(cursor):
    colnames = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return [{colname: value for colname, value in zip(colnames, record)} for record in records]


conn = psycopg2.connect(host='localhost', port='5432', dbname='postgres', user='postgres', password='secret')
cursor = conn.cursor()

# 1. How old were the youngest male and female participants of the 1996 Olympics?
#youngest male
cursor.execute(
    """
    SELECT MIN(Age) FROM athlete_events WHERE Sex = 'M' and Age > 0 and Year = 1996

    """
)
fetch_all(cursor)

#youngest female
cursor.execute(
    """
    SELECT MIN(Age) FROM athlete_events WHERE Sex = 'F' and Age > 0 and Year = 1996

    """
)
fetch_all(cursor)

# 2. What was the percentage of male gymnasts among all the male participants of the 2000 Olympics?
# Round the answer to the first decimal.

cursor.execute(
    """
    SELECT ROUND((COUNT(DISTINCT(athlete_id)) / (SELECT COUNT(DISTINCT(athlete_id))
    FROM athlete_events WHERE sex = 'M' AND year = 2000)::numeric), 3)
        FROM athlete_events
        WHERE sex = 'M' AND year = 2000 AND sport = 'Gymnastics'
    """
)
fetch_all(cursor)

# 3. What are the mean and standard deviation of height for female basketball players participated in the 2000 Olympics?
# Round the answer to the first decimal.

cursor.execute(
    """
    SELECT ROUND((AVG(temp.height)::numeric), 1) AS "avg_height",
    ROUND((STDDEV(temp.height)::numeric), 1) AS "stddev_height"
    FROM (SELECT DISTINCT athlete_id, height FROM athlete_events
    WHERE sex = 'F' AND year = 2000 AND sport = 'Basketball') AS temp
    """
)
fetch_all(cursor)

# 4. Find a sportsperson who participated in the 2002 Olympics,
# with the highest weight among other participants of the same Olympics. What sport did he or she do?

cursor.execute(
    """
   
   
    SELECT Sport FROM athlete_events
        WHERE Year = 2002 and  Weight = (SELECT MAX(Weight) FROM olimpic_new WHERE Year = 2002) Limit 1
    """
)
fetch_all(cursor)

# 5. How many times did Pawe Abratkiewicz participate in the Olympics held in different years?

cursor.execute(
    """
    SELECT COUNT(DISTINCT games)
    FROM athlete_events
    WHERE name = 'Pawe Abratkiewicz'
    """
)
fetch_all(cursor)

# 6. How many silver medals in tennis did Australia win at the 2000 Olympics?
cursor.execute(
    """
SELECT Count(*) FROM athlete_events
     WHERE Medal = 'Silver' and Sport = 'Tennis' and Year = 2000 and Team = 'Australia';

    """
)
fetch_all(cursor)

# 7. Is it true that Switzerland won fewer medals than Serbia at the 2016 Olympics?
# Do not consider NaN values in Medal column.

cursor.execute(
    """
    SELECT team, COUNT(medal) FROM athlete_events
    WHERE medal != 'NA' AND (team = 'Serbia' OR team = 'Switzerland') AND year = 2016
    GROUP BY team
    """
)
fetch_all(cursor)

# 8. What age category did the fewest and the most participants of the 2014 Olympics belong to?

cursor.execute(
    """
    SELECT
        CASE
            WHEN 15 <= age AND 25 > age THEN 15
            WHEN 25 <= age AND 35 > age THEN 25
            WHEN 35 <= age AND 45 > age THEN 35
            WHEN 45 <= age AND 55 >= age THEN 45
        END AS age_group,
    COUNT (DISTINCT athlete_id)
    FROM athlete_events
    WHERE year = 2014
    GROUP BY age_group
    """
)
fetch_all(cursor)

# 9. Is it true that there were Summer Olympics held in Lake Placid?
# Is it true that there were Winter Olympics held in Sankt Moritz?

cursor.execute(
    """
    SELECT city, COUNT(DISTINCT games) FROM athlete_events
    WHERE (city = 'Lake Placid' AND season = 'Summer') OR (city = 'Sankt Moritz' AND season = 'Winter')
    GROUP BY city
    """
)

fetch_all(cursor)


# 10. What is the absolute difference between the number of unique sports at the 1996 Olympics and 2016 Olympics?

cursor.execute(
    """
    SELECT DISTINCT ABS(
        (SELECT COUNT (DISTINCT sport) FROM athlete_events WHERE year = 1996) - 
        (SELECT COUNT (DISTINCT sport) FROM athlete_events WHERE year = 2016)
    )::int AS diff
    FROM athlete_events
    """
)
fetch_all(cursor)
