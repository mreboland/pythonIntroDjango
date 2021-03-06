from django.shortcuts import render, redirect
# Django makes it easy to restrict access to certain pages to logged-in users through the @login_required decorator. A decorator is a directive placed just before a function definition that python applies to the function before it runs, to alter how the function code behaves.
from django.contrib.auth.decorators import login_required
# A 404 response is a standard error response that's returned when a requested resource doesn't exist on a server. We import Http404 which we'll raise if the user requests a topic they shoudn't see.
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Writing a view
# A view function takes in information from a request, prepares the data needed to generate a page, and then sends the data back to the browers, often by using a template that defines what the page will look like.

# The import of render function at the top renders the response based on the data provided by views.

# When a URL request matches the pattern we just defined, django looks for a function called index() in the views.py file. Django then passes the request object to this view function. With no data needing to be processed we call the render() function.
# The render() function passes two arguments. The original request object and a template it can use to build the page. The template will be in index.html
def index(request):
    """The home page for Learning Log"""
    return render(request, "learningLogs/index.html")

# Topics page
# We added topics to our urls.py so we can access by going to /topics in the url.
# We now need to write the topics function to retrieve data from the database and send it to the template.

# We first need to import the model associated with the data we need at the top.
# The topics() function needs one parameter, the request object django received from the server


# We apply login_required() as a decorator to the topics() view function by prepending 
# login_required with the @ symbol. As a result, Python knows to run the code in login_required()
# before the code in topics(). 
# The code in login_required() checks whether a user is logged in, and
# Django runs the code in topics() only if they are. If the user isn’t logged in,
# they’re redirected to the login page.
# To make this redirect work, we need to modify settings.py so Django knows where to find the login page. Add LOGIN_URL = 'users:login' to the very end of settings.py
# After adding the above to settings.py, when an unauthenticated user request a pages protected by the @login_required decorator, django will send the user to the URL defined by LOGIN_URL in settings.py
@login_required
def topics(request):
    """Show all topics"""
    
    # We query the database by asking for the Topic objects, sorted by the dateAdded attribute. We store the resulting queryset in topics var.
    # Currently if we're logged in, we'll be able to see all the topics, no matter which user we're logged in as. We need to update topics below to only show the topics that belong to them.
    # When a user is logged in, the request object has a request.user attribute set that stores info about the user. The query Topic.objects.filter... tells django to retrive only the Topic objects from the database whose owner attribute matches the current user. Because we're not changing how the topics are displayed, we don't need to change the template for the topics page at all.
    topics = Topic.objects.filter(owner=request.user).order_by("dateAdded")
    # We define a context that we'll send to the template. A context is a dictionary in which the keys are names we'll use in the template to access the data, and the values are the data we need to send to the template.
    context = {"topics": topics}
    # When building a page that uses data, we pass the context variable to render() as well as the request object and the path to the template
    return render(request, "learningLogs/topics.html", context)

# The topic view
# The topic() function needs to get the topic and all associated entries from the database

# This is the first view function that requires a param other than the request object. The function accepts the value captured by the expression /<int:topic_id>/ and stores it in topicId
@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries"""
    # We use get() to retrieve the topic, just as we did in the django shell.
    topic = Topic.objects.get(id=topic_id)
    # We get the entries associated with this topic, and we order them according to dateAdded. The minus sign sorts the results in reverse order, the most recent entries first.
    
    # Make sure the topic belongs to the current user.
    # After receiving a topic request, we make sure the topic's user matches the currently logged in user before rendering the page. If the current user doesn't own the requested topic, we raise the Http404 exception and django returns a 404 error page.
    if topic.owner != request.user:
        raise Http404
    
    # of note, in lesson they have topic_set, the topic is the lower case of the second model (class Topic), the one that holds the topics themselves.
    entries = topic.entry_set.order_by("-dateAdded")
    # We store the topic and entries in the context dictionary and send context to the template topic.html
    context = {
        "topic": topic, 
        "entries": entries
        }
    return render(request, "learningLogs/topic.html", context)

# The newTopic() view function 
# As the top we need to import TopicForm from forms.py much like we did with models for our topics. We also import redirect which we use to redirect the user back to the topics page after they submit their topic.


# We use GET requests for pages that only read data from the server. We usually use POST requests 
# when the user needs to submit information through a form.
@login_required
def newTopic(request):
    """Add a new topic"""
    
    # The test below determines whether the request method is GET or POST. It the request method isn't POST, the request is probably GET, so we need to return a blank form (if it's another type of request, a blank form is safe to return).
    if request.method != "POST":
        # No data submitted; create a blank form
        # We make an instance of TopicForm, assign it to a variable, and send the form to the template in the context dictionary at the bottom. Because we didn't include any arguments, django creates a blank form that users can fill out.
        form = TopicForm()
    # If the request method is POST, the else block will run and process the data submitted in the form.
    else:
        # POST data submitted; process data
        
        # We make an instance of TopicForm and pass it the data entered by the user, stored in request.POST. The form object that's returned contains the info submitted by the user.
        form = TopicForm(data=request.POST)
        # We can't save the submitted info in the db until we've checked that it is valid.
        # is_valid() checks that all fields types are filled in (by default all fields must be filled) and that the data entered matches the field types expected (i.e. 200 character limit of CharField)
        if form.is_valid():
            # Currently our page for adding topics is broken because it doesn't associate a new topic with any particular user. It generates a NOT NULL error.
            
            # We call form.save() with the commit=False argument because we need to modify the new topic before saving it to the db.
            newTopic = form.save(commit=False)
            # We then set the new topic's owner attribute to the current user
            newTopic.owner = request.user
            # Finally, we call save() on the topic instance we just defined.
            newTopic.save()
            
            
            # If everything validates, we save the data to the db
            # form.save()
            # Now saved, we can leave the page so we redirect the user back to the topics page
            return redirect("learningLogs:topics")
        
    # Display a blank or invalid form
    

    # The context variable is defined at the end of the view function, and the page is rendered
    # using the template newTopic.html. This code is placed outside of any if block; it will run if
    # a blank form was created, and it will run if a submitted form is determined to be invalid.
    context = {"form": form}
    return render(request, "learningLogs/newTopic.html", context)

# We need to import our EntryForm at the top from forms.py
# The definition of newEntry() has a topic_id param to store the value it receives from the URL


@login_required
def newEntry(request, topic_id):
    """Add a new entry for a particular topic"""
    
    # We'll need the topic to render the page and process the form's data, so we us topic_id to get the correct topic
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    # We check whether the request method is POST or GET. The if block executes if it's a GET request, and we create a blank instance of EntryForm.
    if request.method != "POST":
        # No data submitted; create a blank form
        form = EntryForm()
    else:
        # POST data submitted; process data
        
        # If POST we process the data by making an instance of EntryForm populated with the POST data from the request object
        form = EntryForm(data=request.POST)
        
        # checking if form is valid
        if form.is_valid():
            # If it is, we save it to the db. The commit=False tells django to create a new entry object and assign it to newEntry without saving it the database yet.
            newEntry = form.save(commit=False)
            # We don't save it yet because we need to set the 'topic' attribute of newEntry to the topic we pulled from the database at the beginning of the function. We are taking the topics from class Topic, and linking it to the topics or our newEntry using dot notation
            newEntry.topic = topic
            # Then we call save() with no arguments, saving the entry to the db with the correct associated topic
            newEntry.save()
            # We redirect user back to topic page. The call uses two arguments here, the name of the view we want to redirect to, and an argument that the view function requires. We need the argument topic_id so that the view renders the topic page that the user made an entry for, and they should see their new entry in the list of entries
            return redirect("learningLogs:topic", topic_id=topic_id)
        
    # Display a blank or invalid form
    
    # At the end of the function, we create a context dictionary and render the
    # page using the newEntry.html template. This code will execute for a blank
    # form or for a submitted form that is evaluated as invalid.
    context = {
        "topic": topic,
        "form": form
    }
    return render(request, "learningLogs/newEntry.html", context)


# The editEntry function
# We start by import the class Entry from the models.py
@login_required
def editEntry(request, entry_id):
    """Edit an existing entry"""
    
    # Here we get the entr object that the user wants to edit and the topic associated with the entry.
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    # The editEntry pages have URLs with the entry_id in the URL. This means someone could access it like the topic by doing editEntry/1
    if topic.owner != request.user:
        raise Http404
    
    if request.method != "POST":
        # Initial request; pre-fill form with the current entry
        
        # The instance=entry argument tells django to create the form prefilled with info from the existing entry object. The user will see their existing data and be able to edit that data
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data
        
        # When processing a POST request, we pass the instance=entry argument and the data = request.POST argument. These arguments tell django to create a form instance based on the info associated with the existing entry object, updated with any relevant data from request.POST.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            # We save immediately here because the entry is already associate with the correct topic
            form.save()
            # We redirect to the topic page, where the user should see the updated version of the entry they edited.
            return redirect("learningLogs:topic", topic_id=topic.id)
    
    context = {
        "entry": entry,
        "topic": topic,
        "form": form
    }
    return render(request, "learningLogs/editEntry.html", context)
