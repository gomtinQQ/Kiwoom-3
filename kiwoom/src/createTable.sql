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
        
        
select * from kosdaq where "900"<"901"

select * from kosdaq where "900"= (
	 select "900" from kosdaq where StockCode=900090
	)
	
select "900",StockCode from kosdaq where StockCode=900090