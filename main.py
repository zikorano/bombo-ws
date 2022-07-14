from flask import Flask, request
from errors import api_error
from methods import ops

app = Flask(__name__)

@app.route("/api/players/<operation>", methods=["POST"])
def player_api(operation: str):
    request_args = request.get_json()

    if (operation == "signup"):
        return ops.sign_up(request_args)

    elif (operation == "signin"):
        return ops.sign_in(request_args)

    elif (operation == "signout"):
        return ops.sign_out(request_args)

    elif (operation == "update"):
        return ops.update(request_args)

    elif (operation == "delete"):
        return ops.delete(request_args)

    else:
        return api_error("Invalid operation")

if __name__ == "__main__":
    app.run(debug=True)
