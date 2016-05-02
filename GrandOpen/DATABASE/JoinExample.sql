select * from Relative 
select * from BuyList 

update BuyList set "901" =("9011;0910") where StockCode = 26260

select StockName,StockCode,"901" from BuyList where StockCode = 1840

select A.StockCode,B.StockName from Relative A inner join BuyList B on A.StockCode=B.StockCode where B.BUYSELL="B"

