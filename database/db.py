import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('quiz.db')
    cur = base.cursor()
    if base:
        print('База данных подключена')
    base.execute('CREATE TABLE IF NOT EXISTS questions('
                 'id INTEGER PRIMARY KEY NOT NULL, '
                 'photo TEXT, category TEXT, text TEXT, '
                 'answer_1 TEXT, answer_2 TEXT, answer_3 TEXT, answer_4 TEXT, '
                 'correct_answer TEXT)')
    base.commit()


async def add_question(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO questions (photo, category, text, answer_1, '
                    'answer_2, answer_3, answer_4, correct_answer) '
                    'VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                    tuple(data.values()))
        base.commit()


def get_question():
    return cur.execute(
        'SELECT * FROM questions ORDER BY RANDOM() LIMIT 1').fetchone()
