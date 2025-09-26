from e_commerce.database import connect


def insert_user_register(user_name:str,user_mobile:str, user_email:str ,user_password:str):
    try:
        sql = "insert into user_register (user_name ,user_mobile , user_email , user_password )values(%s ,%s,%s,%s)"
        val = (user_name ,user_mobile ,user_email , user_password )

        mycon , mycur = connect()

        mycur.execute(sql,val)
        mycon.commit()

        if mycur.rowcount:
            return True
        else:
            return False

    except Exception as e:
        print("Error ",e)
        return None 


def get_user_details(user_email,user_password):
    try:
        sql = "select * from  user_register where user_email =%s and user_password = %s"
        val = (user_email , user_password)

        mycon ,mycur = connect()
        mycur.execute(sql,val)
        datas= mycur.fetchone()
        response_data ={
            "user_id":datas[0],
            "user_name":datas[1],
            "user_email":datas[3],
            "user_mobile":datas[2]
        } 

        return response_data
    
    except Exception as e:
        print("User_action.py Error line of 9 : ",e)
        return None
    

def update_user_details(address, city, state, zipcode ,country ,user_id=None):
    try:
        sql = "update user_details set address = %s , city=%s , state = %s , zip_code = %s , country =%s where user_id =%s"
        val=(address , city, state , zipcode ,country ,user_id)

        mycon , mycur = connect()

        mycur.execute(sql,val)
        mycon.commit()
        return True
    
    except Exception as e:
        print("Error in update_user_details : ",e)
        return None

def get_full_details(user_id):
    try:
        sql="""
            select ur.*  , ud.* from user_register ur inner join user_details ud on ud.user_id = ur.user_id where ur.user_id=%s
        """
        val = (user_id,)

        mycon ,mycur =connect()

        mycur.execute(sql,val)
        data = mycur.fetchone()
        return data
    
    except Exception as e:
        print("Error ",e)
        return None

def logout():
    pass