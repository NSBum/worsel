import os
import sys
import sqlite3
import time
from pathlib import Path
from wordle import Trial

conn = None


def _db_path() -> str:
    module_path = Path(__file__).parent.absolute()
    dbpath = os.path.join(module_path, 'rnc.db')
    return dbpath


def _db_connection(path: str) -> sqlite3.Connection:
    if not os.path.exists(path):
        print("ERROR: RNC db does not exist")
        sys.exit(0)
    try:
        conn = sqlite3.connect(path)
    except sqlite3.OperationalError:
        print("ERROR: RNC db cannot be opened")
    return conn


class DB(object):
    def __init__(self):
        # open the database
        path = _db_path()
        self.conn = _db_connection(path)

    def close(self):
        """
        Close db connection
        :return: No return value
        """
        self.conn.close()

    def _db_execute_commit(self, q: str):
        """
        Execute and commit query
        :param q: Query string to execute
        :return: No return value
        """
        cursor = self.conn.execute(q)
        self.conn.commit()

    def candidate_words(self) -> list:
        """
        All useable 5-letter words, excluding some that are poor
        candidates for the puzzle.
        :return: A list of useable words
        """
        q = "SELECT c.lemma FROM corpus c WHERE length(c.lemma) = 5 " \
            "AND NOT c.lemma LIKE '%FALSE%' AND NOT c.lemma LIKE '%-%' "
        cursor = self.conn.execute(q)
        rows = cursor.fetchall()
        lemmas = list(map(lambda x: x[0], rows))
        return lemmas

    def game_in_progress(self) -> bool:
        """
        Is a game currently in progress
        :return: True if a game is in progress, False if not
        """
        q = "SELECT in_progress FROM worsel"
        cursor = self.conn.execute(q)
        return cursor.fetchone()[0]

    def set_game_in_progress(self, flag: bool):
        """
        Sets game in progress flag in db
        :param flag: True if game in progress, Falee if not
        :return: No return value
        """
        f = (lambda: 0, lambda : 1)[flag]()
        q = f"UPDATE worsel SET in_progress = {f}"
        self._db_execute_commit(q)

    def last_game_id(self) -> int:
        """
        Game last played (or currently being played)
        :return: Returns lasy game id in db
        """
        q = "SELECT id FROM game ORDER BY id DESC LIMIT 1"
        cursor = self.conn.execute(q)
        return cursor.fetchone()[0]

    def game_mark_abandoned(self, gid: int):
        """
        Mark game abandoned in db
        :param gid: Game id to mark
        :return: No return vale
        """
        q = f"UPDATE game SET abandoned = 1 WHERE id = {gid}"
        self._db_execute_commit(q)

    def game_mark_solved(self, gid: int, flag: bool):
        """
        Marks game as solved or unsolved
        :param gid: Game id to mark
        :param flag: True if solved, False if no
        :return: No return value
        """
        f = (lambda: 0, lambda: 1)[flag]()
        q = f"UPDATE game SET solved = {f} WHERE id = {gid}"
        self._db_execute_commit(q)

    def game_make_new(self, word: str) -> int:
        """
        Create a new game row in the database
        :param word: The puzzle word for game
        :return: Returns the game id created
        """
        now = int(time.time())
        q = f"INSERT INTO game (time, abandoned, solved, word) VALUES ({now}, 0, 0, '{word}')"
        cursor = self.conn.execute(q)
        self.conn.commit()
        return cursor.lastrowid

    def game_target_word(self, gid: int) -> str:
        """
        The puzzle (target) word for game
        :param gid: Game id to check
        :return: Target word for given game
        """
        q = f"SELECT word from game WHERE id = {gid}"
        cursor = self.conn.execute(q)
        return cursor.fetchone()[0]

    def trials_in_game(self, gid: int) -> list:
        """
        All of the trials for given game
        :param gid: The id of the game being investigated
        :return: A list of Trial objects for this game
        """
        q = f"SELECT * FROM trials WHERE gid = {gid} ORDER BY id ASC"
        cursor = self.conn.execute(q)
        rows = cursor.fetchall()
        trials = []
        for row in rows:
            trial = Trial(row[0], row[2])
            trials.append(trial)
        return trials

    def trial_count_in_game(self, gid: int) -> int:
        """
        Number of trials in game
        :param gid: The id of game being queried
        :return: The count of trials in game.
        """
        q = f"SELECT COUNT(*) FROM trials WHERE gid = {gid}"
        cursor = self.conn.execute(q)
        r = cursor.fetchone()
        return r[0]

    def add_trial_in_game(self, gid: int, word: str):
        """
        Add trial to game
        :param gid: The id of game being modified
        :param word: The word used in the trial
        :return: No return value
        """
        q = f"INSERT INTO trials (gid, word) VALUES ({gid}, '{word}')"
        self._db_execute_commit(q)

    def word_in_dictionary(self, word: str) -> bool:
        """
        Is word in our dictionary?
        :param word: The word being queried
        :return: True if word is in dictionary, False if not
        """
        q = f"SELECT COUNT(*) FROM corpus WHERE lemma LIKE '{word}'"
        cursor = self.conn.execute(q)
        r = cursor.fetchone()
        return r[0] > 0