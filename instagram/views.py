from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Comment,Image,Like,Profile

import cloudinary
import cloudinary.uploader
import cloudinary.api
# Create your views here.
# def welcome(request):
#     return HttpResponse('Welcome to my Instagram Page')

# def welcome(request):
#     return render(request, 'welcome.html')

@login_required(login_url='/accounts/login/')
def welcome(request):
    image = Image.objects.all()
    return render(request, 'home.html', {'image': image})


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search').lower()
        posts = Image.search_by_name(search_term)
        message = f'{search_term}'

        return render(request, 'search.html', {'success': message, 'posts': posts})
    else:
        message = 'You havent searched for any term'
        return render(request, 'search.html', {'danger': message})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    # get images for the current logged in user
    posts = Image.objects.filter(user_id=current_user.id)
    # get the profile of the current logged in user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    return render(request, 'profile.html', {"posts": posts, "profile": profile})


@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':

        current_user = request.user

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        bio = request.POST['bio']

        profile_image = request.FILES['profile_pic']
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image['url']

        user = User.objects.get(id=current_user.id)

        # check if user exists in profile table and if not create a new profile
        if Profile.objects.filter(user_id=current_user.id).exists():
            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_photo = profile_image
            profile.bio = bio
            profile.save()
        else:
            profile = Profile(user_id=current_user.id,
                              profile_photo=profile_url, bio=bio)
            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect('/profile', {'success': 'Profile Updated Successfully'})

       
    else:
        return render(request, 'profile.html', {'danger': 'Profile Update Failed'})

@login_required(login_url='/accounts/login/')
def new_post(request):
    if request.method == 'POST':
        name = request.POST['image_name']
        caption = request.POST['image_caption']
        image_file = request.FILES['image_file']
        image_file = cloudinary.uploader.upload(image_file)
        image_url = image_file['url']
        # image_public_id = image_file['public_id']
        image = Image(image_name=name, image_caption=caption, image=image_url,
                      profile_id=request.POST['user_id'], user_id=request.POST['user_id'])
        image.save_image()
        return redirect('/', {'success': 'Image Uploaded Successfully'})
    else:
        return render(request, 'profile.html', {'danger': 'Image Upload Failed'})

@login_required(login_url='/accounts/login/')
def like_image(request, id):
    likes = Like.objects.filter(post_id=id).first()
    # check if the user has already liked the image
    if Like.objects.filter(post_id=id, user_id=request.user.id).exists():
        # unlike the image
        likes.delete()
        # reduce the number of likes by 1 for the image
        post = Image.objects.get(id=id)
        # check if the image like_count is equal to 0
        if post.likes == 0:
            post.likes = 0
            post.save()
        else:
            post.likes -= 1
            post.save()
        return redirect('/')
    else:
        likes = Like(post_id=id, user_id=request.user.id)
        likes.save()
        # increase the number of likes by 1 for the image
        post = Image.objects.get(id=id)
        post.likes = post.likes + 1
        post.save()
        return redirect('/')

@login_required(login_url='/accounts/login/')
def view_post(request, id):
    image = Image.objects.get(id=id)
    # get related images to the image that is being viewed by the user and order them by the date they were created
    related_posts = Image.objects.filter(
        user_id=image.user_id)
    title = image.name
    # check if image exists
    if Image.objects.filter(id=id).exists():
        # get all the comments for the image
        comments = Comment.objects.filter(image_id=id)
        return render(request, 'post.html', {'image': image, 'comments': comments, 'posts': related_posts, 'title': title})
    else:
        return redirect('/')

@login_required(login_url='/accounts/login/')
def add_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        image_id = request.POST['image_id']
        post = Image.objects.get(id=image_id)
        user = request.user
        comment = Comment(comment=comment, image_id=image_id, user_id=user.id)
        comment.save_comment()
        # increase the number of comments by 1 for the image
        post.comments = post.comments + 1
        post.save()
        return redirect('/post/' + str(image_id))
    else:
        return redirect('/')
        
@login_required(login_url='/accounts/login/')
def user_profile(request, id):
    # check if user exists
    if User.objects.filter(id=id).exists():
        # get the user
        user = User.objects.get(id=id)
        # get all the images for the user
        posts = Image.objects.filter(user_id=id)
        # get the profile of the user
        profile = Profile.objects.filter(user_id=id).first()
        return render(request, 'user-profile.html', {'posts': posts, 'profile': profile, 'user': user})
    else:
        return redirect('/')
