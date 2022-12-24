import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def save(self):
        if not hasattr(self, "id"):
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?,?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            db_dog = CURSOR.execute("select * from dogs order by id desc limit 1").fetchone()
            self.id = db_dog[0]
            return self
    
    def update(self):
        sql = """
            UPDATE dogs
            SET name = (?), breed = (?)
            WHERE id = (?)
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
            

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE if not exists dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)
    @classmethod
    def create(cls, name, breed):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?,?)
        """

        CURSOR.execute(sql, (name, breed))
        dog = cls(name, breed)
        dog.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        dogs = CURSOR.execute("SELECT * FROM dogs")
        return [cls.new_from_db(row) for row in dogs]

    @classmethod 
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs WHERE name = (?) LIMIT 1
        """
        db_dog = CURSOR.execute(sql,(name,)).fetchone()
        if db_dog:
            return cls.new_from_db(db_dog)

    @classmethod
    def find_by_id(cls, dog_id):
        sql = """
            SELECT * FROM dogs WHERE id = (?)
        """
        db_dog = CURSOR.execute(sql, (dog_id,)).fetchone()
        return cls.new_from_db(db_dog)

    @classmethod
    def find_or_create_by(cls, name, breed):
        found = cls.find_by_name(name)
        if not found:
            return cls.create(name, breed)
        elif not found.breed == breed:
            return cls.create(name, breed)
        else: 
            return found