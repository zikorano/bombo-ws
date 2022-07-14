import uuid
from flask import jsonify
from pysondb import db

player_db = db.getDb("db/players.json")

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
        if (len(player_db.getByQuery({"email":email})) == 0):
            # TODO: Generate discriminator for username
            player_id = player_db.add({
                    "email": email,
                    "username": username,
                    "password": password,
                    "activity": {
                         "loggedIn":False,
                         "sessionKey":""
                    }
                })

            response["Message"] = "Player account created succesfully"
            response["Code"] = [200, "Success"]
            response["Content"] = dict(playerID=player_id) 
        
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
        
        results = player_db.getByQuery({"email":email})

        if (len(results) != 0):
            player_id = results[0].get("id")
            # TODO: Open PR in pysondb fixing incorrect return value 
            # type in docstring for db.find() method
            player = player_db.find(player_id)

            if (player["password"] != password):
                response["Message"] = "Password is incorrect. Please confirm and try again"
                response["Code"] = [400, "Bad Request"]
                return jsonify(response)

            player["activity"]["sessionKey"] = str(uuid.uuid1())
            player["activity"]["loggedIn"] = True

            response["Message"] = "Logged in succesfully"
            response["Code"] = [200, "Success"]
            response["Content"] = dict(sessionKey=player["activity"]["sessionKey"])
            player_db.updateById(player_id, {"activity":player["activity"]})

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
        
        results = player_db.getByQuery({"email":email})

        if (len(results) != 0):
            player_id = results[0].get("id")
            player = player_db.find(player_id)

            if (player["password"] != password):
                response["Message"] = "Password is incorrect. Please confirm and try again"
                response["Code"] = [400, "Bad Request"]
                return jsonify(response)

            player["activity"]["sessionKey"] = ""
            player["activity"]["loggedIn"] = False

            response["Message"] = "Logged out succesfully"
            response["Code"] = [200, "Success"]
            player_db.updateById(player_id, {"activity":player["activity"]})

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
        
        results = player_db.getByQuery({"email":email})

        if (len(results) != 0):
            player_id = results[0].get("id")
            player = player_db.find(player_id)

            if (player["password"] != password):
                response["Message"] = "Password is incorrect. Please confirm and try again"
                response["Code"] = [400, "Bad Request"]
                return jsonify(response)
            
            for field, value in payload.items():
                if field in player.keys():
                    player[field] = value

            # Recommend better way of doing this  -> db.updateTableById() or sumn
            for field, value in player.items():
                player_db.updateById(player_id, {field: value})

            response["Message"] = "Player account data updated succesfully"
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
        
        results = player_db.getByQuery({"email":email})

        if (len(results) != 0):
            player_id = results[0].get("id")
            player = player_db.find(player_id)

            if (player["password"] != password):
                response["Message"] = "Password is incorrect. Please confirm and try again"
                response["Code"] = [400, "Bad Request"]
                return jsonify(response)
            
            player_db.deleteById(player_id)

            response["Message"] = "Player account deleted succesfully"
            response["Code"] = [200, "Success"]

        else:
            response["Message"] = "Account with stated email could not be found."
            response["Code"] = [400, "Bad Request"]
        
        return jsonify(response)

if __name__ == "__main__":
    pass