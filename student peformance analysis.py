import sqlite3

# Connect DB
conn = sqlite3.connect("performance.db")
c = conn.cursor()

# Create table
c.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    math INT,
    science INT,
    english INT
)
""")

conn.commit()

# Add student
def add_student():
    name = input("Name: ")
    m = int(input("Math marks: "))
    s = int(input("Science marks: "))
    e = int(input("English marks: "))
    
    c.execute("INSERT INTO students(name, math, science, english) VALUES (?,?,?,?)",
              (name, m, s, e))
    conn.commit()
    print("Student added!")

# Show all students with average + grade
def show_analysis():
    print("\n--- Student Performance ---")
    
    for row in c.execute("SELECT * FROM students"):
        avg = (row[2] + row[3] + row[4]) / 3
        
        if avg >= 90:
            grade = "A"
        elif avg >= 75:
            grade = "B"
        elif avg >= 50:
            grade = "C"
        else:
            grade = "Fail"
        
        print(f"Name: {row[1]}, Avg: {avg:.2f}, Grade: {grade}")

# Topper
def topper():
    c.execute("""
    SELECT name, (math+science+english)/3 as avg
    FROM students
    ORDER BY avg DESC
    LIMIT 1
    """)
    
    t = c.fetchone()
    if t:
        print("\nTopper:", t[0], "Avg:", round(t[1],2))

# Subject-wise average
def subject_analysis():
    c.execute("""
    SELECT AVG(math), AVG(science), AVG(english)
    FROM students
    """)
    
    res = c.fetchone()
    print("\nSubject Averages:")
    print("Math:", round(res[0],2))
    print("Science:", round(res[1],2))
    print("English:", round(res[2],2))

# Menu
while True:
    print("\n1.Add Student")
    print("2.View Performance")
    print("3.Topper")
    print("4.Subject Analysis")
    print("5.Exit")
    
    ch = input("Choice: ")
    
    if ch == "1":
        add_student()
    elif ch == "2":
        show_analysis()
    elif ch == "3":
        topper()
    elif ch == "4":
        subject_analysis()
    elif ch == "5":
        break
    else:
        print("Invalid choice")

conn.close()
