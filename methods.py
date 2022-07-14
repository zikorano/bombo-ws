import uuid
from flask import jsonify
from pysondb import db

user_db = db.getDb("db/users.json")

class ops:
    @staticmethod
    def sign_up(rargs: dict):
        response = {}
        email = rargs.get("email")
        username = rargs.get("username")
        password = rargs.get("password")  

        invalids = list(filter(lambda x: x,
            [(not email), (not username), (not password)]))

        if (len(invalids) > 1):
            response["Message"] = "Several fields are empty, Please fill them and try again"
            response["Code"] = [400, "Bad Request"]
            return jsonify(response)
        
        if (not email):
            response["Message"] = "The 'email' field is empty, Please fill it and try again"
            response["Code"] = [400, "Bad Request"]
            return jsonify(response)

        if (not username):
            response["Message"] = "The 'username' field is empty, Please fill it and try again"
            response["Code"] = [400, "Bad Request"]
            return jsonify(response)

        if (not password):
            response["Message"] = "The 'password' field is empty, Please fill it and try again"
            response["Code"] = [400, "Bad Request"]
            return jsonify(response)


        # Essentially checks if an account has been made with this email 
        if (len(user_db.getByQuery({"email":email})) == 0):
            # TODO: Generate discriminator for username
            user_id = user_db.add({
                    "email": email,
                    "username": username,
                    "password": password,
                    "activity": {
                         "loggedIn":False,
                         "sessionKey":""
                    }
                })

            response["Message"] = "Account created succesfully"
            response["Code"] = [200, "Success"]
            response["Content"] = dict(userId=user_id) 
        
        else:
            response["Message"] = "An account has already been created with this email"
            response["Code"] = [403, "Forbidden: Operation Failed"]

        return jsonify(response)
        
    
    @staticmethod
    def sign_in(rargs: dict):
        response = {}
        email = rargs.get("email")
        password = rargs.get("password")

        if not email:
            response["Message"] = "The 'email' field is empty, Please fill it and try again"
            response["Code"] = [400, "Bad Request"]
            return jsonify(response)
        
        results = user_db.getByQuery({"email":email})

        if (len(results) != 0):
            user_id = results[0].get("id")
            # TODO: Open PR in pysondb fixing incorrect return value 
            # type in docstring for db.find() method
            user = user_db.find(user_id)

            if (user["password"] != password):
                response["Message"] = "Password is incorrect. Please confirm and try again"
                response["Code"] = [400, "Bad Request"]
                return jsonify(response)

            user["activity"]["sessionKey"] = str(uuid.uuid1())
            user["activity"]["loggedIn"] = True

            response["Message"] = "Logged in succesfully"
            response["Code"] = [200, "Success"]
            response["Content"] = dict(sessionKey=user["activity"]["sessionKey"])
            user_db.updateById(user_id, {"activity":user["activity"]})

        else:
            response["Message"] = "Account with stated email could not be found."
            response["Code"] = [400, "Bad Request"]

        return jsonify(response)

    @staticmethod
    def sign_out(rargs):
        response = {}
        email = rargs.get("email")
        password = rargs.get("password")

        if not email:
            response["Message"] = "The 'email' field is empty, Please fill it and try again"
            response["Code"] = [400, "Bad Request"]
            return jsonify(response)
        
        results = user_db.getByQuery({"email":email})

        if (len(results) != 0):
            user_id = results[0].get("id")
            user = user_db.find(user_id)

            if (user["password"] != password):
                response["Message"] = "Password is incorrect. Please confirm and try again"
                response["Code"] = [400, "Bad Request"]
                return jsonify(response)

            user["activity"]["sessionKey"] = ""
            user["activity"]["loggedIn"] = False

            response["Message"] = "Logged out succesfully"
            response["Code"] = [200, "Success"]
            user_db.updateById(user_id, {"activity":user["activity"]})

        else:
            response["Message"] = "Account with stated email could not be found."
            response["Code"] = [400, "Bad Request"]
        
        return jsonify(response)
    
    @staticmethod
    def update(rargs):
        response = {}
        email = rargs.get("email")
        password = rargs.get("password")
        payload = rargs.get("payload")

        if not email:
            response["Message"] = "The 'email' field is empty, Please fill it and try again"
            response["Code"] = [400, "Bad Request"]
            return jsonify(response)
        
        results = user_db.getByQuery({"email":email})

        if (len(results) != 0):
            user_id = results[0].get("id")
            user = user_db.find(user_id)

            if (user["password"] != password):
                response["Message"] = "Password is incorrect. Please confirm and try again"
                response["Code"] = [400, "Bad Request"]
                return jsonify(response)
            
            for field, value in payload.items():
                if field in user.keys():
                    user[field] = value

            # Recommend better way of doing this  -> db.updateTableById() or sumn
            for field, value in user.items():
                user_db.updateById(user_id, {field: value})

            response["Message"] = "User account data updated succesfully"
            response["Code"] = [200, "Success"]

        else:
            response["Message"] = "Account with stated email could not be found."
            response["Code"] = [400, "Bad Request"]
        
        return jsonify(response)
    
    @staticmethod
    def delete(rargs):
        response = {}
        email = rargs.get("email")
        password = rargs.get("password")

        if not email:
            response["Message"] = "The 'email' field is empty, Please fill it and try again"
            response["Code"] = [400, "Bad Request"]
            return jsonify(response)
        
        results = user_db.getByQuery({"email":email})

        if (len(results) != 0):
            user_id = results[0].get("id")
            user = user_db.find(user_id)

            if (user["password"] != password):
                response["Message"] = "Password is incorrect. Please confirm and try again"
                response["Code"] = [400, "Bad Request"]
                return jsonify(response)
            
            user_db.deleteById(user_id)

            response["Message"] = "User account deleted succesfully"
            response["Code"] = [200, "Success"]

        else:
            response["Message"] = "Account with stated email could not be found."
            response["Code"] = [400, "Bad Request"]
        
        return jsonify(response)

if __name__ == "__main__":
    pass