import sqlite3


if __name__ == '__main__':
    
    query = 'create table foo (a text, b text)'
    
    insert = 'insert into foo (a,b) values(?,?)'
    
    strA = '070-2349-3465'
    strB = '060-8587-2342'
    
    str = "select a from ? ;"
    
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    a = 'foo'
    table_name = '070-2349-3465'
#     cursor.execute(query)
    cursor.execute("SELECT * FROM {tn} ".format(tn=a))
    dd = cursor.fetchall()
    print(dd)
    conn.commit()