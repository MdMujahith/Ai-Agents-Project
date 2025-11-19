from tinydb import TinyDB, Query

db = TinyDB('user_memory.json',indent=4, separators=(',', ': '))
mood_table = db.table('mood_logs') # Make sure this matches your table name
Mood = Query()

# Manually setting a past date
test_date = '2025-01-15' 

mood_table.upsert(
    {
        'date': test_date, 
        'mood': 'Stressed', 
        'burnout_score': 8
    }, 
    Mood.date == test_date
)

print(f"Inserted/Updated data for {test_date}")