subjects = {
    "Haladó szintű objektumorientált programozás": 32,
    "Nevezetes algoritmusok és megvalósításuk OOP-technológiával": 32,
    "A tiszta kód elméleti alapjai és gyakorlata": 28,
    "Unit tesztelés": 28,
    "Mobil alkalmazások fejlesztése": 32,
    "Projektmunka": 65,
}

# Do not modify below this line

lesson_number = 1

csv = open("generated.csv", "w", encoding="utf-8")

csv.write(f"Óraszám;Téma\n")

for subject in subjects:
    for i in range(subjects[subject]):
        title = subject

        if (lesson_number + 1) % 10 == 0:
            title = "Összefoglalás"
        elif lesson_number % 10 == 0:
            title = "Számonkérés"

        csv.write(f"{lesson_number};{title}\n")
        lesson_number += 1

csv.close()
