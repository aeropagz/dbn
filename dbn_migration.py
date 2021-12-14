import mariadb
from dummy_data import generate_bank, generate_user


class Migration:
    def __init__(self):
        self._conn = self._get_conn()
        self._conn.autocommit = False
        self.cur = self._conn.cursor()

    def create_user(self):
        user = generate_user()

    def create_user_with_bank(self):
        bank = generate_bank()
        user = generate_user()
        try:
            self.cur.execute(
                "INSERT INTO bank_info (firstname, lastname, iban) VALUES (?, ?, ?)", (
                    bank["firstname"], bank["lastname"], bank["iban"])
            )
            self.cur.execute(
                "INSERT INTO user (nickname, email, bank_info_id) VALUES (?, ?, ?)", (
                    user["username"], user["email"], self.cur.lastrowid
                )
            )
            self.cur.execute("COMMIT")
        except mariadb.Error as e:
            print(f"Error on Insert:{e}")
            print("Rollback")
            self.cur.execute("ROLLBACK")

    def get_ratings(self):

        self.cur.execute(
            "SELECT * FROM rating"
        )

        return self.cur.fetchall()

    def _get_conn(self):
        try:
            conn = mariadb.connect(
                user="klaas",
                password="Dataport202!",
                host="simplelist.de",
                port=3306,
                database="Musik"
            )
        except mariadb.Error as e:
            print(f"Error connecting to db: {e}")
        return conn


if __name__ == "__main__":

    mig = Migration()
    mig.create_user_with_bank()
    
