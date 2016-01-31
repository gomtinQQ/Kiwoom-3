CREATE TABLE `kosdaq` (
	`StockCode`	INTEGER NOT NULL UNIQUE,
	`StockName`	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY(StockCode,StockName)
);


for i in range(9,15):
    for j in range(0,60):
        if j<10:
            j=str(j)
            j=j[:0]+str('0')+j[0:]
        cursor.execute("alter table kosdaq add '"+str(i)+str(j)+"' REAL")