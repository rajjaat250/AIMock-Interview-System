from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Question, Answer
from .serializers import QuestionSerializer


# 🔹 SIGNUP API
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"})

    user = User.objects.create_user(username=username, password=password)
    token = Token.objects.create(user=user)

    return Response({
        "message": "User created successfully",
        "token": token.key
    })


# 🔹 LOGIN API
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Login successful",
            "token": token.key
        })
    else:
        return Response({"error": "Invalid credentials"})


# 🔹 GET QUESTIONS (by role)
@api_view(['GET'])
def get_questions(request):
    role = request.GET.get('role')

    if not role:
        return Response({"error": "Role is required"})

    questions = Question.objects.filter(role=role)
    serializer = QuestionSerializer(questions, many=True)

    return Response(serializer.data)


# 🔹 SUBMIT ANSWER + SCORING
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request):

    user = request.user
    question_id = request.data.get('question_id')
    answer_text = request.data.get('answer')

    if not question_id or not answer_text:
        return Response({"error": "Missing data"})

    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({"error": "Question not found"})

    # 🔥 KEYWORD MATCH LOGIC
    keywords = question.keywords.split(',')

    score = 0
    for word in keywords:
        if word.strip().lower() in answer_text.lower():
            score += 1

    # Save answer
    Answer.objects.create(
        user=user,
        question=question,
        answer_text=answer_text,
        score=score
    )

    return Response({
        "message": "Answer submitted",
        "score": score
    })