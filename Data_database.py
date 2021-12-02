import sqlite3

def log_data(name, date, uuid, serial_number, firmware_version, BT_reads, fob_reads, jumper, failure, notes):
    con = sqlite3.connect('database/data.db')
    cur = con.cursor()

    try:
        # Create table
        cur.execute('''CREATE TABLE logs (name text, date text, uuid text,  serial_number text, firmware_version text, BT_reads 
        text, fob_reads text, jumper text, failure text, notes text)''')
    except:
        print("Table existed")
    # The qmark style used with executemany():
    lang_list = [
        (name, date, uuid, serial_number, firmware_version, BT_reads, fob_reads, jumper, failure, notes),
    ]
    cur.executemany("INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?,?)", lang_list)

    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()

if __name__ == "__main__":
    log_data()