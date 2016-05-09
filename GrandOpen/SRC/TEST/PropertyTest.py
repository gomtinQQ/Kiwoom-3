# -*- coding: utf-8 -*-

if __name__ == '__main__':

    sRQName  = "주식주문" # 사용자 구분 요청 명 
    sScreenNo = "0101" #화면번호[4]
    ACCNO="234f23f;23f".replace(';','')    #계좌번호
    nOrderType = 1      #1신규매수 2신규매도 3매수취소 4매도취소 5매수정정 6매도정정
    
    nQty  = 10          #주문수량
    nPrice  = 0         #주문단가
    sHogaGb  = '03'   #0:지정가, 3:시장가, 5:조건부지정가, 6:최유리지정가, 7:최우선지정가, 10:지정가 IOC, 13:시장가IOC, 16:최유리IOC, 20:지정가FOK, 23:시장가FOK, 26:최유리FOK, 61:시간외 단일가매매, 81:시간외종가
    sOrgOrderNo  = "" #원주문번호
    
    print(sRQName,sScreenNo,ACCNO,nOrderType,nQty,nPrice,sHogaGb,sOrgOrderNo)
    print(type(sRQName),type(sScreenNo),type(ACCNO),type(nOrderType),type(nQty),type(nPrice),type(sHogaGb),type(sOrgOrderNo))
    
    
    volume=''
    print(len(volume))
    if len(volume)==0:
        volume='0'
    print(int(volume))