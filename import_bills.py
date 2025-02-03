import pandas as pd
from prisma import Prisma

# Initialize Prisma Client
db = Prisma()

async def import_data():
    await db.connect()

    # Load CSV data
    df = pd.read_csv("bills_formatted.csv")

    # Convert data to dictionary format for bulk insert
    records = df.to_dict(orient="records")

    # Insert records into the database
    await db.bill.create_many(data=records)

    print("Data imported successfully!")

    await db.disconnect()

# Run the import function
import asyncio
asyncio.run(import_data())
