from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Author, Category,Book, Comment, LikeList, UserProfile
from rango.forms import CategoryForm,UserForm, UserProfileForm,BookForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

#help function ->get cookie
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request,name):
    #!!!username cookie！！！
    username = str(get_server_side_cookie(request,'username',name))
    request.session['username'] = username


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



# show all book in a specific category
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
            return redirect(reverse('rango:operator_index'))
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
            # Will handle the bad form, new form, or no form supplied cases.
            # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

#add a book in a specific category
@login_required
def add_book(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
        
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:operator_index'))
    #get info from BookForm
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        author_name = request.POST.get('author_name')
        author = Author.objects.get_or_create(name = author_name)[0]
        author.save()

        if form.is_valid():
            if category:
                book = form.save(commit=False)
                book.category = category
                book.views = 0
                book.author = author
                if 'image' in request.FILES:
                    book.image = request.FILES['image']
                book.save()
                return redirect(reverse('rango:operator_show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form':form, 'category': category}

    return render(request, 'rango/add_book.html', context=context_dict)

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                visitor_cookie_handler(request,username)
                userprofile = UserProfile.objects.get(user=user)
                if userprofile.role == "USER":
                    return redirect(reverse('rango:index'))
                elif userprofile.role == "OPERATOR":
                    return redirect(reverse('rango:operator_index'))
                elif userprofile.role == "ADMIN":
                    return redirect(reverse('rango:admin_index'))
                
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

# show book detail 
def show_book(request, book_name_slug):
    username = request.session.get('username')
    comment_num = 0
    score_sum = 0
    context_dict = {}
    try:
        book = Book.objects.get(slug=book_name_slug)
        book.views += 1
        book.author.views += 1
        book.author.save()
        book.save()
        context_dict['book'] = book
        # get comment from comment table by book 
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
# change the favorite button's style!
# if user had favorite the book, the button should show "remove", if not, show "ADD"
    if username != None:
        user = User.objects.get(username=username)
        datas = LikeList.objects.filter(user=user)

        #change the style by sent style's class as context
        if datas.exists():
            for data in datas:
                books = data.favoriteBook.all()
                for every_book in books:
                    if every_book.title == book.title:
                        context_dict['button_content'] = 'Remove from my favorite'
                        context_dict['button_style'] = 'btn btn-success'
                        return render(request, 'rango/book.html', context=context_dict)
                context_dict['button_content'] = 'Add to my favorite'
                context_dict['button_style'] = 'btn btn-outline-success'
                return render(request, 'rango/book.html', context=context_dict)
        else:
            context_dict['button_content'] = 'Add to my favorite'
            context_dict['button_style'] = 'btn btn-outline-success'
    
    return render(request, 'rango/book.html', context=context_dict)

#can be used when login as user.
@login_required
def add_comment(request, book_name_slug):

    if request.method == 'POST':
        username = request.session.get('username')
        score = request.POST.get('btnradio')
        content = request.POST.get('content')

        user = User.objects.get(username=username)
        book = Book.objects.get(slug=book_name_slug)
 
        comment = Comment.objects.get_or_create(user=user, book=book)[0]
        comment.score = score
        comment.content = content
        comment.save()

    return redirect(reverse('rango:show_book', kwargs={'book_name_slug': book_name_slug}))


# show user's favorite list page
@login_required
def my_favorite(request, username):
    context_dict = {}
    user = User.objects.get(username=username)
    datas = LikeList.objects.filter(user=user)
    for data in datas:
        context_dict['books'] = data.favoriteBook.all()
    return render(request, 'rango/favorite.html', context=context_dict)

#a help functoin to add a book to favorite list 
@login_required
def add_favorite(request, book_name_slug):
    if request.method == 'POST':
        username = request.session.get('username')
        user = User.objects.get(username=username)
        book = Book.objects.get(slug=book_name_slug)
        datas = LikeList.objects.filter(user=user)
        if datas.exists():
            for data in datas:
                books = data.favoriteBook.all()
                for every_book in books:
                    if every_book.title == book.title:
                        data.favoriteBook.remove(every_book)
                        return redirect(reverse('rango:show_book', kwargs={'book_name_slug': book_name_slug}))
                data.favoriteBook.add(book)
                return redirect(reverse('rango:show_book', kwargs={'book_name_slug': book_name_slug}))
        else:
            likelist = LikeList.objects.get_or_create(user=user)[0]
            likelist.save()
            likelist.favoriteBook.add(book)

    return redirect(reverse('rango:show_book', kwargs={'book_name_slug': book_name_slug}))


#show operator's homepage, just like user homepage,with out some function.
@login_required
def operator_index(request):
    # get all info for index page
    category_list = Category.objects.all()
    context_dict = {}
    context_dict['categories'] = category_list
    
    response = render(request, 'rango/operator_index.html', context=context_dict)
    return response

#show books in specific category,
@login_required
def operator_show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        
        books = Book.objects.filter(category=category)
       
        context_dict['books'] = books
     
        context_dict['category'] = category
    except Category.DoesNotExist:
       
        context_dict['category'] = None
        context_dict['books'] = None
   
    return render(request, 'rango/operator_category.html', context=context_dict)

#a help function, delet a category.
#!!!!! if delete a category, all book in this category will be deleted auto!!!
@login_required
def operator_delete_category(request,category_name_slug):
    category = Category.objects.get(slug=category_name_slug)
    category.delete()
    category_list = Category.objects.all()
    context_dict = {}
    context_dict['categories'] = category_list
    
    response = render(request, 'rango/operator_index.html', context=context_dict)
    return response

# a help function, delete a book, search the book by its slug name
@login_required
def operator_delete_book(request,book_name_slug):
    book = Book.objects.get(slug=book_name_slug)
    book.delete()
    if request.method == 'POST':
        category_name_slug = request.POST.get('category')
    
    return redirect(reverse('rango:operator_show_category', kwargs={'category_name_slug': category_name_slug}))
    
#admin homepage, send a context contain two string,"USER","OPERATOR". to indentify which url to redirect.
@login_required
def admin_index(request):
    context_dict = {}
    context_dict['operator_style'] = "OPERATOR"
    context_dict['user_style'] = "USER"
    return render(request, 'rango/admin_index.html', context=context_dict)

#jump to specfic url, indentify the url by the KEY WORDS post in this functon
@login_required
def admin_modify_user(request, role):
    context_dict={}
    users = UserProfile.objects.filter(role = role)
    context_dict['role'] = role
    context_dict['users'] = users
    return render(request, 'rango/admin_modify_user.html', context=context_dict)

# modify user, for now, just delete it.
@login_required
def admin_delete_user(request, user_name):
    operator = User.objects.get(username=user_name)
    operator.delete()
    return redirect(reverse('rango:admin_index'))

#a help function, to implement the search function, use Jacascript and AJAX
def search(request):
    title = request.GET.get('title')
    books = Book.objects.filter(title__contains=title)
    context_dict={}
    context_dict['books'] = books
    context_dict['title'] = title
    rejson = []
    for book in books:
        rejson.append(book.title)

    if "search" in request.GET:
        return render(request, 'rango/search_books.html', context=context_dict)
    elif "operator_search" in request.GET:
        return render(request, 'rango/operator_search_books.html', context=context_dict)
    else:
        return HttpResponse(json.dumps(rejson), content_type='application/json')

#admin can add an operator by this function, just like register a user.
@login_required
def admin_add_operator(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.role = 'OPERATOR'
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
    return render(request, 'rango/admin_add_operator.html', context={'user_form':user_form,'profile_form':profile_form, 'registered':registered})


#show books wrote by specific author.
def show_author_books(request, author_name):
    context_dict = {}
    try:
        author = Author.objects.get(name=author_name)
        
        books = Book.objects.filter(author=author)
       
        context_dict['books'] = books
     
        context_dict['author'] = author
    except Category.DoesNotExist:
       
        context_dict['category'] = None
        context_dict['author'] = None
   
    return render(request, 'rango/author_books.html', context=context_dict)
