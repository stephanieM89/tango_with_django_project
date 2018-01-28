from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page


def index(request):
    # The following is changed during chapter 6
    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # Query the database for a list of ALL categories currently stored
    # Order the categories by no likes in descending order
    # Retrieve the top 5 only - or all if less than 5
    # Place the list in our context_dict dictionary that'll be passed to template engine

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # chapter 4, remove the following line
    # return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
    # replace with a pointer to the about.html template
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







