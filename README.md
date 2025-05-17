[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=19559505)
# **Django Pagination Hands-On Group Activity**  
**Objective:** Create a Django project, populate a model with AI-generated data, and implement pagination to display records efficiently.  

## **Activity Overview**  
- **Duration:** 30 minutes  
- **Group Size:** 2 learners per group  
- **Prerequisites:** Basic Python knowledge, Django installed (`pip install django`)  
- **Tools Needed:** Python, Django, Browser, AI Tool (e.g., ChatGPT, Mockaroo)  


## **Step-by-Step Instructions**  

### **1. Create a New Django Project**  
**Guidelines:**  
1. Open a terminal and run:  
   ```bash
   django-admin startproject pagination_project
   cd pagination_project
   python manage.py startapp books
   ```
2. Add `'books'` to `INSTALLED_APPS` in `settings.py`.  
3. Run migrations:  
   ```bash
   python manage.py migrate
   ```

### **2. Define a Single Model**  
**Task:** Create a `Book` model with fields:  
- `title` (CharField)  
- `author` (CharField)  
- `published_year` (IntegerField)  

```python
# books/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField()

    def __str__(self):
        return self.title
```
- Register the model in `admin.py`:  
  ```python
  from django.contrib import admin
  from .models import Book
  admin.site.register(Book)
  ```
- Run:  
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```


### **3. Populate the Model with AI-Generated Data**  
**Option 1: Use ChatGPT**  
- Prompt: *"Generate 50 fake book records in JSON format with title, author, and published_year."*  
- Save the output as `books.json` in a `fixtures` folder.  
- Load data:  
  ```bash
  python manage.py loaddata books.json
  ```

**Option 2: Use Mockaroo**  
- Visit [Mockaroo](https://www.mockaroo.com/) and configure fields:  
  - `title` (Book Title)  
  - `author` (Full Name)  
  - `published_year` (Number, 1900-2023)  
- Download as JSON and load as above.  


### **4. Implement Pagination**  
#### **Step 1: Create a View**  
```python
# books/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book

def book_list(request):
    books = Book.objects.all().order_by('title')
    paginator = Paginator(books, 5)  # 5 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/book_list.html', {'page_obj': page_obj})
```

#### **Step 2: Add URL**  
```python
# pagination_project/urls.py
from django.contrib import admin
from django.urls import path
from books.views import book_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', book_list, name='book_list'),
]
```

#### **Step 3: Create a Template**  
```html
<!-- books/templates/books/book_list.html -->
<h1>Book List</h1>
<ul>
  {% for book in page_obj %}
    <li>{{ book.title }} ({{ book.published_year }}) by {{ book.author }}</li>
  {% endfor %}
</ul>

<div class="pagination">
  <span class="step-links">
    {% if page_obj.has_previous %}
      <a href="?page=1">&laquo; first</a>
      <a href="?page={{ page_obj.previous_page_number }}">previous</a>
    {% endif %}

    <span class="current">
      Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
    </span>

    {% if page_obj.has_next %}
      <a href="?page={{ page_obj.next_page_number }}">next</a>
      <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
    {% endif %}
  </span>
</div>
```

### **5. Test & Discuss**  
- Run the server:  
  ```bash
  python manage.py runserver
  ```
- Visit `http://127.0.0.1:8000/books/` and navigate pages.  
- **Discussion Questions:**  
  - Why is pagination important for large datasets?  
  - How would you customize items per page dynamically?  
  - What happens if `page` is invalid?  


## **Bonus Challenges**  
**Dynamic Items Per Page:** Add a dropdown to change `per_page` value.  
**Styled Pagination:** Use Bootstrap for better UI.  
**Search + Pagination:** Filter books by author/year before paginating.  


## **Conclusion**  
Learners will:  
- Set up a Django project from scratch.
- Populate a model using AI tools.
- Implement and customize pagination.  

**Happy Coding!** 
