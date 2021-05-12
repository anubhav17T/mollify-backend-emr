# from databases import Database
# from constants.const import DB_URL
#
# database = Database(DB_URL)
#
#
# async def connect():
#     await database.connect()
#
#
# # Create a table.
# async def create_table():
#     query = """CREATE TABLE HighScores (id INTEGER PRIMARY KEY, name VARCHAR(100), score INTEGER)"""
#     await database.execute(query=query)
#     # Insert some data.
#     query = "INSERT INTO HighScores(name, score) VALUES (:name, :score)"
#     values = [
#         {"name": "Daisy", "score": 92},
#         {"name": "Neil", "score": 87},
#         {"name": "Carol", "score": 43},
#     ]
#     await database.execute_many(query=query, values=values)
#     # Run a database query.
#     query = "SELECT * FROM HighScores"
#     rows = await database.fetch_all(query=query)
#     print('High Scores:', rows)
#
#
#
#
# import asyncio
# loop = asyncio.get_event_loop()
# loop.run_until_complete(create_table())
# loop.close()


search = "all"

if search is "true" or search is "false":
    print("yes")
else:
    print("false")