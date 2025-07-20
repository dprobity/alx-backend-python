import asyncio
import aiosqlite

DB_FILE = "my_database.db"

async def async_fetch_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All users:")
            for user in users:
                print(user)
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in older_users:
                print(user)
            return older_users
        

async def fetch_concurrently():

    try:
        all_users, older_users = await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users()
        )

        results = {
            "all_users": all_users,
            "older_users": older_users
        }

        #### we can just return or go further and process the results here, maybe decide to do an aggregation or something that makes sense

        return results
    
    except Exception as e:
        print(f"An error occured during the concurrent check: {e}")





if __name__ == "__main__":
    asyncio.run(fetch_concurrently)
