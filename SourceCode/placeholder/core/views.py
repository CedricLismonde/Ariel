from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Recipe, LikeRecipe,FollowersCount,Comment
from itertools import chain

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    for usernames in user_following_list:
        feed_lists = Recipe.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))
    #print(feed)

    #posts= Recipe.objects.all()
    return render(request,'index.html',{'user_profile':user_profile,
                                        'posts':feed_list
                                        }
                  
                  )    

#the goal is when you click on comment you see the post/recipe that you want to comment an another page
#
'''
def comment(request):
    recipe_id = request.GET.get("recipe_id")
    recipe=Recipe.objects.get(recipe_id=recipe_id)
    
    post=[]
    post.append(recipe)

    
    context ={'posts':post, 
              }
    
    return render(request,'comment.html',context)
'''

def comment(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    recipe_id = request.GET.get("recipe_id")
    recipe=Recipe.objects.get(recipe_id=recipe_id)
    
    post=[]
    post.append(recipe)
    
    comments=[]
    comments_of_recipe=Comment.objects.filter(recipe_id=recipe_id)
    comments.append(comments_of_recipe)
    comment_list= list(chain(*comments))
    
    context ={'posts':post,
              'comment_list':comment_list,
              'user_profile':user_profile
              }
    
    return render(request,'comment.html',context)


@login_required(login_url='signin')
def uploadCom(request):
    if request.method == 'POST':
        recipe_id = request.POST['recipe_id']
        user = request.user.username
        txt = request.POST['comment_txt']
        
        new_comment = Comment.objects.create(user=user,
                                             recipe_id=recipe_id,
                                             txt=txt
                                             )
        new_comment.save()
        return redirect('/comment?recipe_id='+recipe_id)
        
    else:
        return redirect('/')

###

@login_required(login_url='signin')
def upload(request):
    
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        recipe_title = request.POST['recipe_title']
        recipe_text = request.POST['recipe_text']
        
        new_recipe = Recipe.objects.create(user=user,
                                           image=image,
                                           recipe_title=recipe_title,
                                           preparation_step=recipe_text
                                           )
        new_recipe.save()
        return redirect('/')
        
    else:    
        return redirect('/')



@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    recipe_id = request.GET.get("recipe_id")
    
    recipe=Recipe.objects.get(recipe_id=recipe_id)
    
    like_filter = LikeRecipe.objects.filter(post_id=recipe_id,
                                            username=username
                                            ).first()
    if like_filter == None:
        new_like = LikeRecipe.objects.create(post_id=recipe_id,
                                             username=username
                                             )
        new_like.save()

        recipe.nb_likes = recipe.nb_likes+1
        recipe.save()
        return redirect('/')
    else:
        like_filter.delete()
        recipe.nb_likes = recipe.nb_likes-1
        recipe.save()
        return redirect('/')

def search(request):
    #if request.method =="POST":
    #    request.POST['']
    
    return render(request, 'search.html')

@login_required(login_url='signin')
def follow(request):
    if request.method =='POST':
        follower= request.POST['follower']
        user= request.POST['user']
        
        if FollowersCount.objects.filter(follower=follower,
                                         user=user).first():
            
               FollowersCount.objects.filter(follower=follower,
                                             user=user).delete()
               return redirect('/profile/'+user)
        else:
           new_follower = FollowersCount.objects.create(follower=follower,
                                                        user=user)
           new_follower.save()
           return redirect('/profile/'+user)
            
    else:   
        return redirect('/')
        

@login_required(login_url='signin')
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Recipe.objects.filter(user=pk)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk
    
    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text ='Unfollow'
    else:
        button_text='follow'
    
    nbr_user_followers =len(FollowersCount.objects.filter(user=pk))
    nbr_user_following =len(FollowersCount.objects.filter(follower=pk))
    
    context = {
            'user_object': user_object,
            'user_profile': user_profile,
            'user_posts': user_posts,
            'user_post_length':user_post_length,
            'button_text': button_text,
            'nbr_user_followers':nbr_user_followers,
            'nbr_user_following':nbr_user_following
        }
    return render(request, 'profile.html',context)

@login_required(login_url='signin')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)
    
    if request.method =='POST':
        
        if request.FILES.get('image') ==None:
            image=user_profile.profile_picture #
        else:
            image=request.FILES.get('image')
            
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        #must do for the correct fields
            
        user_profile.firstname=firstname
        user_profile.lastname=lastname
        user_profile.profile_picture=image
        user_profile.email=email
        user_profile.save()
        
        return redirect('settings')
        
    return render(request,'setting.html',{'user_profile': user_profile})

def signup(request):

    if request.method =='POST':
        username=   request.POST['username']
        email=      request.POST['email']
        firstname=  request.POST['firstname']
        lastname=   request.POST['lastname']
        password1=  request.POST['password1']
        password2=  request.POST['password2']
        if password1==password2:
            if User.objects.filter(email=email).exists(): 
                messages.info(request,'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,
                                               email=email,
                                               password=password1
                                               #,
                                               #firstname=firstname,
                                               #lastname=lastname          
                                               )
                user.save()
                
                #log user in and redirect to settings page
                user_login =auth.authenticate(username=username,
                                              password=password1)
                auth.login(request,user_login)
                
                #create a profile objcet for the new user
                user_model = User.objects.get(username=username)
                    #maybe add fname and all
                new_profile = Profile.objects.create(user=user_model,
                                                     id_user=user_model.id,
                                                     firstname=firstname,
                                                     lastname=lastname,
                                                     email=email
                                                     )
                new_profile.save()
                
                return redirect('settings')
                
        else:
            messages.info(request,'Password not matching')
            return redirect('signup')
    
    else:
        return render(request,'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,
                                password=password
                                )
        '''  
        print(username,password,user)
        if user is None:
            user = auth.authenticate(email=username,
                                    password=password
                                    )
            
        print(username,password,user)
        '''
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'user does not exist')
            return redirect('signin')
        
    else:
        return render(request,'signin.html')
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')






#1:46:00
#@login_required(login_url='signin')