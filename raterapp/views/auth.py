"""Authentication Module"""
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from raterapp.models import Player

User = get_user_model()

@csrf_exempt
def login_user(request):
    """Handle the authentication of a Gamer

    Method arguments:
        request -- The full HTTP request object
    """

    req_body = json.loads(request.body.decode())

    # If the request is an HTTP POST, pull out relevant information
    if request.method == 'POST':

        # verify using the builtin authenticate method
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication successful, respond with the token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({ "valid": True, "token": token.key })
            return HttpResponse(data, content_type='application/json')

        # Credentials did not match existing user, cannot log user in
        else:
            data = json.dumps({ "valid": False })
            return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_user(request):
    """Handle registration of a new User - will create a User and a Player

    Method arguments:
        request -- The full HTTP request object
    """

    # Get the POST body
    req_body = json.loads(request.body.decode())

    # Create a new User via the create_user helper method from Django's User model
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    # Create a new Gamer to pair with this User
    player = Player.objects.create(
        bio=req_body['bio'],
        user=new_user
    )

    # Commit the gamer to the database by explicitly saving
    player.save()

    # Generate a new token for the new user using REST framework's token generator
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({ "token": token.key })
    return HttpResponse(data, content_type="application/json")
