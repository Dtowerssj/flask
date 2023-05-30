import MetaTrader5 as mt5
from forex_python.converter import CurrencyRates

lot = 0.1

def getPipValue(symbol):
    account_currency = 'USD'
    symbol_1 = symbol[0:3]
    symbol_2 = symbol[3:6]
    c = CurrencyRates()
    return c.convert(symbol_2, account_currency, c.convert(symbol_1, symbol_2, 1))

def calculate_lot(risk, balance, slSize, symbol):
    print(risk, balance, slSize, symbol)
    #pip_value = getPipValue(symbol)
    pip_value = 10
    print("Valor de pip: ", pip_value)

    moneyRisk = balance*(risk/100)

    lot = round(moneyRisk / (slSize * pip_value), 2) 

    print("Lotaje calculado: ", format(lot))

    return lot

def open_buy(trade_info, risk, balance):
    global lot
    symbol_info = ''
    symbol = trade_info[0]
    tp = trade_info[2]
    sl = trade_info[3]

    # attempt to enable the display of the symbol in MarketWatch
    """ print(symbol[5])
    selected=mt5.symbol_select(symbol,True)
    if not selected:
        print("Failed to select ", symbol)
        mt5.shutdown()
        quit() """

     # prepare the buy request structure
    symbol_info = mt5.symbol_info(symbol)
    #print(symbol_info)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check() = ", mt5.last_error())
        quit()
        mt5.shutdown() 
    
    # display symbol symbol properties
    symbol_info=mt5.symbol_info(symbol)
    if symbol_info!=None:
        # display the terminal data 'as is'    
        print("{}: spread = {},  digits = {}".format(symbol,symbol_info.spread, symbol_info.digits))
        # display symbol properties as a list
        #print("Show symbol_info(\"{}\")._asdict():".format(symbol))
        symbol_info_dict = mt5.symbol_info(symbol)._asdict()
        for prop in symbol_info_dict:
            print("  {}={}".format(prop, symbol_info_dict[prop]))
    
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()
    
    
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20

    # Find the filling mode of symbol
    filling_type = mt5.symbol_info(symbol).filling_mode
    filling_type2 = mt5.ORDER_FILLING_FOK


    slSize = (price - sl)*100
    lot = calculate_lot(float(risk), float(balance), slSize, symbol)

    if symbol == 'XAGUSD' or symbol == 'EURUSD' or 'XAUUSD':
        slSize = (price - sl)*1000
        lot = calculate_lot(float(risk), float(balance), slSize, symbol)
        if symbol == 'XAGUSD':
            lot = 2*(calculate_lot(float(risk), float(balance), slSize, symbol))
        if symbol == 'XAUUSD':
            slSize = (price - sl)*10
            lot = calculate_lot(float(risk), float(balance), slSize, symbol)


    position_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": "Rio script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling_type - 1,
    }
    
    # send a trading request
    result = mt5.order_send(position_request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        quit()
        return
    
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))

def open_sell(trade_info, risk, balance):
    
    symbol_info = ''
    symbol = trade_info[0]
    print("El simbolo es: "+symbol)
    tp = trade_info[2]
    sl = trade_info[3]

    

    """  # get all symbols
    symbols=mt5.symbols_get()
    
 
    if symbols is None:
        print(mt5.last_error())
        mt5.shutdown()
        quit()
    
    print('Symbols: ', len(symbols))
    count=0
    # display the first five ones
    for s in symbols:
        count+=1
        print("{}. {}".format(count,s.name))
        if count==5: break
    print() """
    
    # prepare the buy request structure
    symbol_info = mt5.symbol_info(symbol)
    #print(symbol_info)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check(): ", mt5.last_error())
        mt5.shutdown()
        quit()
    
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()
     
    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    # attempt to enable the display of the asdfer symbol in MarketWatch 
    selected=mt5.symbol_select(symbol,True) 
    if not selected: 
        print("failed to select, error code =",mt5.last_error())
        mt5.shutdown() 
        quit() 
    
    # display symbol properties 
    symbol_info=mt5.symbol_info(symbol) 
    if symbol_info!=None: 
        # display the terminal data 'as is'  
        print(symbol, ": spread =",symbol_info.spread,"  digits =",symbol_info.digits) 
        # display symbol properties as a list 
        print("Show symbol_info(\"{}\")._asdict():", symbol) 
        symbol_info_dict = mt5.symbol_info(symbol)._asdict() 
        for prop in symbol_info_dict: 
            print("  {}={}".format(prop, symbol_info_dict[prop]))
    else: 
        print("Failed to symbol info ", symbol) 
  
    if symbol == 'XAGUSD' or symbol == 'EURUSD' or 'XAUUSD':
        slSize = (price - sl)*1000
        lot = calculate_lot(float(risk), float(balance), slSize, symbol)
        if symbol == 'XAGUSD':
            lot = 2*(calculate_lot(float(risk), float(balance), slSize, symbol))
        if symbol == 'XAUUSD':
            slSize = (price - sl)*10
            lot = calculate_lot(float(risk), float(balance), slSize, symbol)

    point = symbol_info.point
    price = symbol_info.bid
    deviation = 20

    # Find the filling mode of symbol
    filling_type = mt5.symbol_info(symbol).filling_mode
    filling_type2 = mt5.ORDER_FILLING_FOK

    """ print(mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_BOC, mt5.ORDER_FILLING_RETURN)
    print(filling_type)
    print(filling_type - 1) """

    slSize = (sl - price)*1000
    lot = calculate_lot(float(risk), float(balance), slSize, symbol)

    position_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling_type - 1,
    }
    
    # send a trading request
    result = mt5.order_send(position_request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        quit()
    
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order)) 

def close_position(symbol_text):
    price = ''
    global lot

    symbol = symbol_text
    positions = mt5.positions_get(symbol=symbol)
    print(positions)
    position_id= positions[0][0]
    lot = positions[0][9] # lotaje de la posicion abierta
    position_type = positions[0][5] # compra o venta de la posicion abierta

    if position_type == 0: # Si es una compra, ejecuta venta para cerrar
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    elif position_type == 1: # Si es una venta, ejecuta compra para cerrar
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    else: 
        print('No se pudo detectar si es un a venta o una compra ')
        exit()
    
    # create a close request
    deviation=20
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    print(request)
    # send a trading request
    result=mt5.order_send(request)
    # check the execution result
    print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result",result)
    else:
        print("4. position #{} closed, {}".format(position_id,result))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()

def modify_sl(symbol, sl):
    
    symbol = symbol
    sl = sl
    global lot

    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print("Posicion {} no encontrada".format(symbol))
        quit()

    position_id= positions[0][0]
    position_type = positions[0][5] # compra o venta de la posicion abierta
    price_open = positions[0][10]
    tp = positions[0][11]

    if position_type == 0: # Si es una compra, ejecuta venta para cerrar
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    elif position_type == 1: # Si es una venta, ejecuta compra para cerrar
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    else: 
        print('No se pudo detectar si es un a venta o una compra ')
        exit()

    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": symbol,
        # "volume": lot,
       # "type": trade_type,
        "position": int(position_id),
       # "price_open": price_open,
        "sl": float(sl),
        "deviation": 20,
        "magic": 234000,
        "comment": "python script open",
        #"type_time": mt5.ORDER_TIME_GTC,
        #"type_filling": mt5.ORDER_FILLING_FOK,
        #"ENUM_ORDER_STATE": mt5.ORDER_FILLING_RETURN,
    }
    #// perform the check and display the result 'as is'
    result = mt5.order_send(request)

    print(result)

    print(mt5.last_error())
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))

        print(" result",result)