def session_login(request):
   if request.method == "POST":
       username = request.POST.get('username') 
       password = request.POST.get('password') 

       try:
          user=User.objects.get(username=username)

          if user.check_password(password):
            request.session['user_id'] = user.id 
            request.session['username'] = user.username 
            request.session['email'] = user.email 
            return redirect(session_dashboard)
          else: 
                return HttpResponse("Invalid Password")
       except User.DoesNotExist: 
            return HttpResponse("User does not exist")
   return render(request, 'login.html')


def session_dashboard(request):
    username_session = request.session.get('username') 
    if 'username' in request.session:
        return render(request, 'dashboard.html',{'username': username_session}) 
    else: 
        return redirect('session_login')
    


 <h1>Welcome {{ request.session.username }}</h1>
    <p>Email: {{ request.session.email }}</p>


def session_logout(request):
    request.session.flush()
    return redirect('session_login')

 path('session_logout',views.session_logout,name="session_logout"),

<a href="{% url 'session_logout' %}">LOGOUT</a>