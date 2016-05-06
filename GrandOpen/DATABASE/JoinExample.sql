select * from Relative 
select * from BuyList 

update BuyList set "901" =("9011;0910") where StockCode = 26260

select StockName,StockCode,"901" from BuyList where StockCode = 1840

select A.StockCode,B.StockName,A."900",B."900",B."901",B."956" 
from Relative A join BuyList B on A.StockCode=B.StockCode 
where B.BUYSELL="N"  and B."956"=-3860 

select * from BuyList where  StockCode="51370"  order by 

SELECT sql FROM sqlite_master
WHERE tbl_name = 'BuyList' AND type = 'table'

PRAGMA table_info(BuyList)