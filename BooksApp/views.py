from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import Book

# Create your views here.

    
@csrf_exempt
def home(request):     # http request
    print(request.method)
    if request.method == "POST":
        bid = request.POST.get("book_id")
        Name = request.POST.get("book_name")
        Quantity = request.POST.get("book_qty")
        Price = request.POST.get("book_prc")
        Author = request.POST.get("book_author")
        Is_Published = request.POST.get("book_is_published")
        # print(Name, Quantity, Price, Author, Is_Published)
        if Is_Published == "Yes":
            Is_Published = True
        else:
            Is_Published = False

        if not bid:
            Book.objects.create(name = Name, qty = Quantity, price = Price, author = Author, is_published = Is_Published)
        else:
            book_obj = Book.objects.get(id = bid)
            book_obj.name = Name
            book_obj.qty = Quantity
            book_obj.price = Price
            book_obj.author = Author
            book_obj.is_published = Is_Published
            book_obj.save()


        # return redirect("home_page")
        return HttpResponse("Success")
    elif request.method == "GET":
        # print(request.GET)              #to get query parameter
        return render(request, "home.html", {"person_name": "Arin"})


def show_books(request):
    return render(request, "show_books.html", {"books" : Book.objects.filter(is_active=True), "active": True})


def update_book(request, pk):
    book_obj = Book.objects.get(id = pk)
    return render(request, "home.html", {"single_book":book_obj})


def delete_book(request, pk):                      #hard delete
    book_obj = Book.objects.get(id = pk).delete()
    return redirect("all_active_books")


def soft_delete_book(request, pk):
    book_obj = Book.objects.get(id = pk)
    book_obj.is_active = False
    book_obj.save()
    return redirect("all_inactive_books")


def show_inactive_books(request):
    return render(request, "show_books.html", {"books" : Book.objects.filter(is_active=False), "inactive": True})


def restore_book(request, pk):
    book_obj = Book.objects.get(id = pk)
    book_obj.is_active = True
    book_obj.save()
    return redirect("all_active_books")


from .forms import BookForm, AddressForm
# from django.contrib.auth.forms import UserCreationForm

def book_form(request):
    form = BookForm()
    if request.method == 'POST':
        print(request.POST)
        form = BookForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Successfully Registered!!!")
    else:
        context = {'form': form}
        return render(request, "book_form.html", context=context)



# simlpeisbetterthancomplex

# def simple(request):
#     return render(request, "simple.html", {"form": AddressForm()})

import csv

def create_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="test.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['name','qty','price','author','is_published','is_active'])

    books = Book.objects.all().values_list('name','qty','price','author','is_published','is_active')
    for book in books:
        writer.writerow(book)
    return response



import xlwt
from .models import Book

def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="test1.xls"'

    wb = xlwt.Workbook(response)
    ws = wb.add_sheet('text_data',cell_overwrite_ok=True)

    row_num = 0

    columns = ['name','qty','price','author','is_published','is_active']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num])


    books = Book.objects.all().values_list('name','qty','price','author','is_published','is_active')
    for row in books:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])
    wb.save(response)
    return response




from django.db import connection
def raw_query_csv(request):
    response = HttpResponse(content_type = 'test/csv')
    response['content-Disposition'] = 'attachment; filename = "raw_query_csv.csv"'
    writer = csv.writer(response)
    cursor = connection.cursor()
    cursor.execute('''select * from book''')
    data = cursor.fetchall()
    for book in data:
        writer.writerow(book)
    return response




def upload_csv(request):
    file = request.FILES["csv_file"]
    data = file.read().decode('utf-8').splitlines()
    expected_header_lst = ['name', 'qty', 'price', 'author', 'is_published']
    expected_header_lst.sort()

    actual_header_lst = data[0].split(",")
    actual_header_lst.sort()

    if expected_header_lst != actual_header_lst:
        return HttpResponse("Error...headers are not equal...!")

    reader = csv.DictReader(data)         # always use dict reader
    lst = []
    for element in reader:
        is_pub = element.get("is_published")
        if is_pub == "True":
            is_pub = True 
        else:
            is_pub = False
        
        lst.append(Book(name=element.get("name"), qty=element.get("qty"), price=element.get("price"), author= element.get("author"),is_published = is_pub ))
        # print(lst)
    Book.objects.bulk_create(lst)
    return HttpResponse("Success")
   



