import mysql.connector

vocab = ["system", "fire", "service", "protect", "security", "alarm", "extinguish", "emergency", "provide", "safety", "suppress", "solution", "communicate", "inspect", "design",
        "control", "custom", "maintain", "build", "install", "life", "quality", "monitor", "time", "need", "sprinkler", "safe", "hazard", "repair"]

# Connect to your MySQL database
conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='929268',
        database='aipro'
)

# Create a cursor
cursor = conn.cursor()

# Insert words into the table
for word in vocab:
    cursor.execute("INSERT INTO vocabulary (word) VALUES (%s)", (word,))

# Commit changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
