from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from .models import *
import os
from django.conf import settings
from pathlib import Path
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.
@login_required(login_url='/')
def home(request, unique):
    user_content = []
    date_now = datetime.now()
    if str(request.user) == str(unique):
        
        for content in Content.objects.all():
            if Followed.objects.filter(my_id = request.user.id, followed_id = content.writer_id):
                user_content += [
                    UserContents(
                    name = User.objects.get(id = content.writer_id).username, 
                    first_name = User.objects.get(id = content.writer_id).first_name, 
                    last_name = User.objects.get(id = content.writer_id).last_name, 
                    content = content.content,
                    date = content.date,
                    title = content.title, 
                    image = ProfileImg.objects.get(user_id = content.writer_id).image,
                    content_id= content.id
                    )]
            elif content.writer_id == request.user.id:
                user_content += [
                    UserContents(
                    name = User.objects.get(id = content.writer_id).username, 
                    first_name = User.objects.get(id = content.writer_id).first_name, 
                    last_name = User.objects.get(id = content.writer_id).last_name, 
                    content = content.content,
                    date = content.date,
                    title = content.title, 
                    image = ProfileImg.objects.get(user_id = content.writer_id).image,
                    content_id= content.id
                    )]
        return render(request, 'home.html', {
            'contents':user_content,
            'date':date_now 
            })
    else:
        return HttpResponseBadRequest()
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        data_user = [username, password]


        user = auth.authenticate(username = username, password=password)

        if user is not None:
            auth.login(request, user)
            print("username :", user, "is just login") 
            return redirect(f'/home/{request.user}', {"data" : data_user})
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/')
    else:      
        return render(request, 'login.html') 
def logout(request):
    print("username :", request.user, "is just logout")
    auth.logout(request)
    return redirect('/')
def register(request):
    if request.method == 'POST':
        username    = request.POST['username']
        first_name  = request.POST['first_name']
        last_name   = request.POST['last_name']
        email       = request.POST['email']
        password    = request.POST['password']
        password2   = request.POST['password2']

        if password == password2 and len(username) != 0 and len(password) != 0 and len(email) != 0:
            
            if User.objects.filter(username=username).exists() or User.objects.filter(email = email).exists():
                messages.info(request, 'Username already use')
                return redirect('register')
            else:
                try:
                    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email = email)
                    user.save()

                    # Set Profile Image to default
                    profileimage = ProfileImg.objects.create(
                        user_id = user.id
                        )
                    profileimage.save()

                except Exception as e:
                    print(e)

                print("Welcome new user", user)
                return redirect('login')
        else:
            messages.info(request, 'Password is not the same')
            return redirect('register')
    else:
        return render(request, 'register.html')
def post(request, unique):
    if request.method == "POST":
        
        content = request.POST.get('content')
        title = request.POST.get('title')

        if len(str(content)) > 0 and len(str(title)) > 0:
            if str(request.user) == str(unique):
                new_content = Content.objects.create(content = content, title = title, writer_id = request.user.id)
                new_content.save()
                return redirect(f'/home/{request.user}')
            else:
                return HttpResponseBadRequest()
            
        else:
            messages.info(request, 'Error!! No content to post')
            return redirect(f'/home/{request.user}/post')
    else:
        return render(request, 'post.html')  
def profile(request, username):
    have_profile = None
    user_content = []
    is_login = False
    already_follow = False
    if str(request.user) != str(username):
        data_user = User.objects.get(username=username)
        already_follow = Followed.objects.filter(my_id = request.user.id, followed_id = data_user.id).exists()

        #Untuk Foto Profil
        image = ProfileImg.objects.get(user_id = data_user.id).image
        print(str(image) == 'default-profile.jpg')
        if str(image) == 'default-profile.jpg': # Kondisi ketika foto profil tidak ada
            image = False

        # Untuk Konten
        for content in Content.objects.filter(writer_id = data_user.id):
            user_content += [
                UserContents(
                name = User.objects.get(id = content.writer_id).username, 
                content = content.content,
                date = content.date,
                title = content.title,
                content_id = content.id 
                )]
            if User.objects.get(id = content.writer_id).username == str(request.user):
                is_login = True
        return render(request, 'profile.html', {'datauser':data_user, 'contents':user_content, 'is_login':is_login, 'profileimg':image, 'already_follow' : already_follow})
    else:
        data_user = User.objects.get(username = str(request.user))

        #Untuk Foto Profil
        image = ProfileImg.objects.get(user_id = request.user.id).image
        print(str(image) == 'default-profile.jpg')
        if str(image) == 'default-profile.jpg': # Kondisi ketika foto profil tidak ada
            image = False

        # Untuk Konten
        for content in Content.objects.filter(writer_id = data_user.id):
            user_content += [
                UserContents(
                name = User.objects.get(id = content.writer_id).username, 
                content = content.content,
                date = content.date,
                title = content.title,
                content_id = content.id 
                )]
        return render(request, 'profile.html', {'datauser':data_user, 'contents':user_content, 'is_login':True, 'profileimg':image})
def uploadimg(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        if ProfileImg.objects.filter(user_id = request.user.id).exists():
            # Menghapus File Image
            old_image = ProfileImg.objects.get(user_id = request.user.id)
            old_file = os.path.join(settings.MEDIA_ROOT, str(old_image.image))
            old_image.delete()
            try:
                os.remove(old_file)
            except Exception as e:
                print(e)

            # Upload Image baru setelah di hapus
            uploadimage = ProfileImg.objects.create(image = image, user_id = request.user.id)
            uploadimage.save()
            return redirect(f'profile/{request.user}')
        else:
            uploadimage = ProfileImg.objects.create(image = image, user_id = request.user.id)
            uploadimage.save()
            return redirect(f'profile/{request.user}')
    else:  
        return redirect(f'profile/{request.user}')
def content(request, username, id):
    comments = []
    # if request.method == 'POST':
    user_content = UserContents(
        name = username,
        content = Content.objects.get(id = id, writer_id = User.objects.get(username = username).id).content,
        date = Content.objects.get(id = id, writer_id = User.objects.get(username = username).id).date,
        title = Content.objects.get(id = id, writer_id = User.objects.get(username = username).id).title,
        content_id = id,
        first_name = User.objects.get(username = username).first_name,
        last_name = User.objects.get(username = username).last_name,
        image = ProfileImg.objects.get(user_id = User.objects.get(username = username).id).image
    )
    

    for comment in Comment.objects.filter(content_id = id):
        comments += [CommentContent(
            comment = Comment.objects.get(id = comment.id).comment,
            name = User.objects.get(id = comment.user_id).username,
            date = Comment.objects.get(id = comment.id).date,
            first_name = User.objects.get(id = comment.user_id).first_name,
            last_name = User.objects.get(id = comment.user_id).last_name,
            image = ProfileImg.objects.get(user_id = comment.user_id).image
        )
        ]


    return render(request, 'content.html', {
            'content':user_content,
            'user':user_content,
            'comments': comments,
            'me':str(request.user),
        })
def comment(request, username, id):
    comments = []
    if request.method == 'POST':
        comment = request.POST.get('comment')
        content_id = request.POST['content_id']
        user_id = request.POST['user_id']

        content = Content.objects.get(id = content_id)
        if len(comment) > 0 :
            new_comment = Comment.objects.create(comment = comment, content_id = content_id, user_id = user_id)
            new_comment.save()

        for comment in Comment.objects.filter(content_id = content_id):
            comments += [CommentContent(
                comment = Comment.objects.get(id = comment.id).comment,
                name = User.objects.get(id = comment.user_id).username,
                date = Comment.objects.get(id = comment.id).date,
                first_name = User.objects.get(id = comment.user_id).first_name,
                last_name = User.objects.get(id = comment.user_id).last_name,
                image = ProfileImg.objects.get(user_id = comment.user_id).image
            )
            ]

        return redirect(f'/content/{username}/{id}', {
            'content':content,
            'name':username,
            'comments': comments,
            'me':str(request.user)
        })
@csrf_exempt
def search(request, keyword):
    
    list_username = []
    list_first_name = []
    list_last_name = []

    list_user = []
    images = []
    if len(str(keyword)) > 0:
        key = keyword
        key = key.split()
        
        for search_key in key:
            for all_user in User.objects.all():
                list_username += [all_user.username]
                list_first_name  += [all_user.first_name ]
                list_last_name += [all_user.last_name]

            for usernames in list_username:
                if str(search_key).lower() in str(usernames).lower() :
                    for user in User.objects.filter(username = usernames):
                        list_user += [UserContents(
                            name = user.username,
                            first_name = user.first_name,
                            last_name= user.last_name,
                            image = ProfileImg.objects.get(user_id = user.id).image
                        )]
            for first_names in list_first_name:
                if str(search_key).lower() in str(first_names).lower() :
                    for user in User.objects.filter(first_name = first_names):
                        list_user += [UserContents(
                            name = user.username,
                            first_name = user.first_name,
                            last_name= user.last_name,
                            image = ProfileImg.objects.get(user_id = user.id).image
                        )]
            for last_names in list_last_name:
                if str(search_key).lower() in str(last_names).lower() :
                    for user in User.objects.filter(last_name = last_names):
                        list_user += [UserContents(
                            name = user.username,
                            first_name = user.first_name,
                            last_name= user.last_name,
                            image = ProfileImg.objects.get(user_id = user.id).image
                        )]
        index = []
        print(len(list_user))
        for i in range(len(list_user)):
            for j in range(i + 1, len(list_user)):
                if i == len(list_user):
                    break
                if list_user[i].name == list_user[j].name:
                    index += [j]  
        index = set(index)
        index = sorted(index, reverse=True)
        for i in index:
            list_user.remove(list_user[i])
  
        return render(request, 'search.html', {'list_user' : list_user, 'search_key':search_key})
    else:
        return redirect(f'/home/{request.user}')
def follow(request, followed_id):
    already_follow = Followed.objects.filter(my_id = request.user.id, followed_id = followed_id).exists()
    if not already_follow:
        new_follower = Followed.objects.create(my_id = request.user.id, followed_id = followed_id)
        new_follower.save()
    else:
        old_follower =  Followed.objects.get(my_id = request.user.id, followed_id = followed_id)
        old_follower.delete()


    username = User.objects.get(id = followed_id).username
    return redirect(f'/profile/{username}')
class UserContents():
    def __init__(self, name='', content='', date='', title='', content_id=0, first_name = '', last_name = '', image = 'default/default-profile.jpg', is_follow = False) -> None:
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.content = content
        self.date = date
        self.title = title
        self.content_id = content_id
        self.is_follow  = is_follow

        # addition function for image
        if len(str(image)) == len('default-profile.jpg') :
            self.image = 'default/default-profile.jpg'
        else:
            self.image = image
class CommentContent():
    def __init__(self, comment, name, date, first_name = '', last_name = '',image = 'default/default-profile.jpg') -> None:
        self.comment = comment
        self.name = name
        self.date = date
        self.first_name = first_name
        self.last_name = last_name
        if len(str(image)) == len('default-profile.jpg') :
            self.image = 'default/default-profile.jpg'
        else:
            self.image = image
        