from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    # The following is changed during chapter 6
    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # Query the database for a list of ALL categories currently stored
    # Order the categories by no likes in descending order
    # Retrieve the top 5 only - or all if less than 5
    # Place the list in our context_dict dictionary that'll be passed to template engine

    category_list = Category.objects.order_by('-likes')[:5]

    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # chapter 4, remove the following line
    # return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
    # replace with a pointer to the about.html template

    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out user name, if no one is logged it prints AnonymousUser
    print(request.user)

    return render(request, 'rango/about.html', {})


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to template rendering engine
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrive all of the associated pages.
        # Note that filer() returns a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # Adds out results list to the template context under name pages
        context_dict['pages'] = pages
        # Add the category object from the database to the context dictionary.
        # Will use this in the template to verify that the category exists
        context_dict['category'] = category

        # If didn't find the specific category, don't do anything
        # The template will display the "no category" message for us
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

        # Go render the response and return it to the client
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=True)
            print(category, category.slug)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially.  Code changes value to True when registration succeeds
    registered = False

    # If its a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            # Save the user's form data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method
            # Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            # Sort out the user profile instance
            # Since we need to set the user attribute outselves, we set commit = False.
            # This delays ssaving the model until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did user provide a profile picture? If so, need to get it from the input
            # form and put it in the UserProfile model

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            # update our variable to indicate that the template registration was successful
            registered = True
        else:

            # invalid form or forms = mistakes or something else?
            # print problems to the terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not a http post, so we render our form using 2 ModelForm instances
        # These forms will be blank, ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form,
                                                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


# Use the login_required() decorator to ensure only those logged in can access the view
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
