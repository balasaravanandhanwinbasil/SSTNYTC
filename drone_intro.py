import pyhula
import time

# create an instance of the UserApi class from the pyhula library
uapi = pyhula.UserApi()

# connect to the drone's wifi network

if not uapi.connect():
    print("Connection error")
else:
    print('Connection to station by WiFi')
    uapi.single_fly_takeoff()
    uapi.single_fly_up(10)

    i = 0
    result = uapi.single_fly_recognition_Qrcode(0,0)
    while i < 10 and result['result'] != True: 
        time.sleep(0.1)
        i += 1 
        result = uapi.single_fly_recognition_Qrcode(0,0)
        print(result)
        
        if result['result'] == True:
            uapi.single_fly_lamplight(0,0,255,10,1)
            break
    
    uapi.single_fly_touchdown()
            
        
    

 


'''api.single_fly_Qrcode_align(mode =0 , qr_id =0) 
api.single_fly_forward(50)
are_we_there = api.single_fly_recognition_QrCode(mode=0, qr_id=1)
if are_we_there == True:
    api.single_fly_lamplight(255,0,5,1)
api.single_fly_touchdown()'
'''


