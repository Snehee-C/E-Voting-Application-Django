from django.http import Http404,HttpResponseForbidden
from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from .forms import ContactForm
from .models import Notice, Question, Choice

def HomePage(request):
    return render(request, 'homepage.html')

def contact(request):
    return render(request,"contact.html")

def validate_password(password):
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in "_@$!#%^&*()-[]{?}><" for c in password)
    return has_upper and has_lower and has_digit and has_symbol

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        if not uname.isdigit() or len(uname) != 10:
            return HttpResponse("Username should be a 10-digit number.")

        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if len(pass1) < 6 or not validate_password(pass1):
            return HttpResponse("Password < 6 and doesn't satisfy all conditions: Uppercase, Lowercase, Symbol, and Digit")

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')  
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username.isdigit() or len(username) != 10:
            return HttpResponse("Username should be a 10-digit number.")
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('votespage')  
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')

def votespage(request):
    question = Question.objects.first()  
    return render(request, "voting.html", {'question': question})
 

def register(request):
    return render(request, "register.html")


def notice(request):
    notices = Notice.objects.all()
    return render(request, 'notice.html', {'notices': notices})


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'voting.html', {'question': question})

def results(request):
    all_choices = Choice.objects.all()
    vote_counts = []
    for choice in all_choices:
        vote_counts.append({
            'choice_text': choice.choice_text,
            'votes': choice.votes
        })
    
    question = Question.objects.first()  
    
    return render(request, 'result.html', {'vote_counts': vote_counts, 'question': question})

def vote(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     has_voted = request.session.get(f'voted_{question_id}', False)
    
     if has_voted:
         return HttpResponseForbidden("You have already voted for this question.")

     if request.method == 'POST':
         try:
             selected_choice = question.choice_set.get(pk=request.POST['choice'])
         except (KeyError, Choice.DoesNotExist):
             return render(request, 'voting.html', {'question': question, 'error_message': "You didn't select a choice."})
         else:
             selected_choice.votes += 1
             selected_choice.save()

             request.session[f'voted_{question_id}'] = True
             request.session.modified = True
             return redirect('result')

     if has_voted:
         return redirect('result')

     return render(request, 'voting.html', {'question': question})



def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})

    
