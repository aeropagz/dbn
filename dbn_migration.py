from math import exp
import random
import mariadb
import time
from dummy_data import generate_bank, generate_user, generate_playlist


class Migration:
    def __init__(self):
        self._conn = self._get_conn()
        self._conn.autocommit = False
        self.cur = self._conn.cursor()

    def create_rating(self, rat_per_song: int):
        try:
            self.cur.execute(
                "SELECT id from user"
            )

            users = [row[0] for row in self.cur.fetchall()]
            self.cur.execute(
                "SELECT id from song"
            )
            song_ids = [row[0] for row in self.cur.fetchall()]
            random.shuffle(song_ids)
            for song_id in song_ids:
                for i in range(rat_per_song):
                    user = random.choice(users)
                    rating = random.randint(3,5)
                    try:
                        self.cur.execute(
                            "INSERT INTO rating (rating, user_id, song_id) VALUES (?, ?, ?)",
                            (rating, user, song_id)
                        )
                        self.cur.execute("COMMIT")
                    
                    except mariadb.Error as e:
                        print(f"Error on creating rating: {e}")
                        print("Rolling back changes")
                        self.cur.execute("ROLLBACK")

            

        except mariadb.Error as e:
            print(f"Error on creating rating: {e}")
            print("Rolling back changes")
            self.cur.execute("ROLLBACK")

    def create_playlist(self, n):
        try:
            self.cur.execute("SELECT id, nickname from user")
            users = self.cur.fetchall()
            self.cur.execute("SELECT id from song")
            song_ids = self.cur.fetchall()
            for i in range(n): 
                user = random.choice(users)
                playlist_name = generate_playlist(user[1])
                self.cur.execute(
                    "INSERT INTO playlist (name, user_id) VALUES (?, ?)",
                    (playlist_name, user[0]),
                )
                playlist_id = self.cur.lastrowid
                songs_in_playlist = random.choices(song_ids, k=random.randint(1, 15))
                for song_id in songs_in_playlist:
                    self.cur.execute(
                        "INSERT INTO playlist_has_song (playlist_id, song_id) VALUES (?, ?)",
                        (playlist_id, song_id[0])
                )
            self.cur.execute("COMMIT")
        except mariadb.Error as e:
            print(f"Error on Insert playlist: {e}")
            print("Rollback actions")
            self.cur.execute("ROLLBACK")


    def create_user_with_bank(self):
        bank = generate_bank()
        user = generate_user()
        try:
            self.cur.execute(
                "INSERT INTO bank_info (firstname, lastname, iban) VALUES (?, ?, ?)",
                (bank["firstname"], bank["lastname"], bank["iban"]),
            )
            self.cur.execute(
                "INSERT INTO user (nickname, email, bank_info_id) VALUES (?, ?, ?)",
                (user["username"], user["email"], self.cur.lastrowid),
            )
            self.cur.execute("COMMIT")
        except mariadb.Error as e:
            print(f"Error on Insert:{e}")
            print("Rollback")
            self.cur.execute("ROLLBACK")

    def get_ratings(self):

        self.cur.execute("SELECT * FROM rating")

        return self.cur.fetchall()

    def _get_conn(self):
        try:
            conn = mariadb.connect(
                user="klaas",
                password="Dataport202!",
                host="simplelist.de",
                port=3306,
                database="Musik",
            )
        except mariadb.Error as e:
            print(f"Error connecting to db: {e}")
        return conn


if __name__ == "__main__":
    random.seed(int(time.time())/23)
    mig = Migration()
    mig.create_rating(5)
