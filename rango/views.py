from django import urls
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import title
from rango.models import Author, Category,Book, Comment, LikeList
from rango.forms import CategoryForm,UserForm, UserProfileForm,BookForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def index(request):
    # get all info for index page
    category_list = Category.objects.all()
    book_list = Book.objects.order_by('-views')[:5]
    author_list = Author.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['books'] = book_list
    context_dict['authors'] = author_list
    
    response = render(request, 'rango/index.html', context=context_dict)
    return response
    #return render(request, 'rango/index.html', context=context_dict)


def about(request):
    visitor_cookie_handler(request)
    context_dict = {'boldmessage': "This tutorial has been put together by <Chi Zhang>.",
                    'visits':request.session.get('visits'),
                    }
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        
        books = Book.objects.filter(category=category)
       
        context_dict['books'] = books
     
        context_dict['category'] = category
    except Category.DoesNotExist:
       
        context_dict['category'] = None
        context_dict['books'] = None
   
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect(reverse('rango:index'))
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
            # Will handle the bad form, new form, or no form supplied cases.
            # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))

    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            if category:
                Book = form.save(commit=False)
                Book.category = category
                Book.views = 0
                Book.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', context={'user_form':user_form,'profile_form':profile_form, 'registered':registered})


def user_login(request):
    print(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        print("no post")
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def show_book(request, book_name_slug):
    comment_num = 0
    score_sum = 0
    context_dict = {}
    try:
        book = Book.objects.get(slug=book_name_slug)
        context_dict['book'] = book
        try:
            comments = Comment.objects.filter(book=book).order_by('-date')
            for comment in comments:
                comment_num +=1
                score_sum += int(comment.score)
            if comment_num == 0:
                context_dict['score_ave'] = 'No mark for now!'
            else:
                score_ave = score_sum/comment_num
                context_dict['score_ave'] = str(score_ave)
            context_dict['comments'] = comments
        except Comment.DoesNotExist:
            context_dict['comments'] = None
    except Book.DoesNotExist:
        context_dict['book'] = None
   
    return render(request, 'rango/book.html', context=context_dict)

def add_comment(request, book_name_slug):

    if request.method == 'POST':
        username = request.POST.get('username')
        score = request.POST.get('score')
        content = request.POST.get('content')

        user = User.objects.get(username=username)
        book = Book.objects.get(slug=book_name_slug)
 
        comment = Comment.objects.get_or_create(user=user, book=book)[0]
        if Comment.objects.get_or_create(user=user, book=book)[1]:
            comment.score = score
            comment.content = content
            comment.save()
        else:
            pass
    return redirect(reverse('rango:show_book', kwargs={'book_name_slug': book_name_slug}))

def my_favorite(request, username):
    context_dict = {}
    user = User.objects.get(username=username)
    datas = LikeList.objects.filter(user=user)
    for data in datas:
        context_dict['books'] = data.favoriteBook.all()
        print("=======================")
        print(data)
    return render(request, 'rango/favorite.html', context=context_dict)

