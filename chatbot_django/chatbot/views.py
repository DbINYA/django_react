from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import User

from .ml_model import ML_MODEL, answer_print
from .models import Chat
from .forms import MessageForm, MessageUpdateForm
from .serializers import ChatSerializer


def chatbot_response(message):

    output = ML_MODEL.run(
        "meta/llama-2-7b-chat",
        input={"prompt": message}
    )

    return answer_print(output)


@api_view(['GET', 'POST'])
def chatbot_answer(request):
    if request.method == 'GET':

        chat_history = Chat.objects.filter(user=request.user)

        return render(request, 'chatbot.html', {"chat_history": chat_history})

    if request.method == 'POST':

        form = MessageForm(request.data)

        if form.is_valid():

            message = form.data["message"]
            response = chatbot_response(message)
            chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
            chat.save()

            return redirect("chatbot_url")

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def delete_message(request, message_id):

    message = get_object_or_404(Chat, pk=message_id)

    if message.user != request.user:
        return Response({'error': 'Вы не автор этого сообщения.'}, status=status.HTTP_403_FORBIDDEN)

    message.delete()

    return redirect("chatbot_url")


@api_view(['GET', 'POST'])
def update_message(request, message_id):

    obj = get_object_or_404(Chat, pk=message_id)

    if request.method == 'POST':
        form = MessageUpdateForm(request.POST)

        if form.is_valid():

            message = form.data["message"]
            response = chatbot_response(message)

            obj.message = message
            obj.response = response
            obj.created_at = timezone.now()
            obj.save()

            return redirect("chatbot_url")

    if request.method == "GET":
        return render(request, "form.html", {"chat": obj.message.strip()})

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("chatbot_url")
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect("login")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect("chatbot_url")
            except:
                error_message = "Error creating account"
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Passwords are not equal"
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')