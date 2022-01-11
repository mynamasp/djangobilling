import datetime
import random

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from .models import Menu, Customers
from .utils import getmenu, getcustomer, calculate_discount


# Create your views here.
def refresh_data():
    Menu.objects.all().delete()
    Customers.objects.all().delete()

    menu_dict = getmenu()

    for i in menu_dict:
        product_ID = i
        product_name = menu_dict[i][0]
        product_rate_1 = menu_dict[i][1]
        product_rate_2 = menu_dict[i][2]
        product_rate_3 = menu_dict[i][3]

        m = Menu.objects.create(product_ID=product_ID, product_name=product_name, product_rate_1=product_rate_1,
                                product_rate_2=product_rate_2,
                                product_rate_3=product_rate_3)
        m.save()

    customer_dict = getcustomer()

    for i in customer_dict:
        customer_id = i
        customer_name = customer_dict[i][0]
        customer_phone_no = customer_dict[i][1]

        m = Customers.objects.create(customer_ID=customer_id, customer_name=customer_name,
                                     customer_phone_no=customer_phone_no)

        m.save()


def home_view(request):
    context = {'logged': False}
    request.session['prod_list_created'] = True
    total = 0
    print(request.POST)

    try:
        cust_ph_no = request.POST['ph_number']
        customer_query = Customers.objects.filter(customer_phone_no__exact=cust_ph_no)
        context['cust_name'] = customer_query[0].customer_name
        context['cust_id'] = customer_query[0].customer_ID
        context['ph_no'] = cust_ph_no
        context['logged'] = True
        request.session['ph_no'] = request.POST['ph_number']
        request.session['guest'] = False
        request.session['prod_list'] = []

    except IndexError:
        cust_ph_no = request.POST['ph_number']
        context['cust_name'] = 'Guest'
        context['cust_id'] = 'Guest'
        context['ph_no'] = cust_ph_no
        context['logged'] = True
        request.session['ph_no'] = cust_ph_no
        request.session['guest'] = True
        request.session['prod_list'] = []

    except:
        pass

    if not context['logged']:
        try:
            if not request.session['guest']:
                cust_ph_no = request.session['ph_no']
                customer_query = Customers.objects.filter(customer_phone_no__exact=cust_ph_no)
                context['cust_name'] = customer_query[0].customer_name
                context['cust_id'] = customer_query[0].customer_ID
                context['ph_no'] = cust_ph_no
                context['logged'] = True

            else:
                context['ph_no'] = request.session['ph_no']
                context['cust_name'] = 'Guest'
                context['cust_id'] = 'Guest'
                context['logged'] = True


        except:
            pass

    if context['logged']:
        product_id = []
        product_name = []
        product_rate1 = []
        product_rate2 = []
        product_rate3 = []

        product_query = Menu.objects.all()
        for i in product_query:
            product_id.append(i.product_ID)
            product_name.append(i.product_name)
            product_rate1.append(i.product_rate_1)
            product_rate2.append(i.product_rate_2)
            product_rate3.append(i.product_rate_3)
            context["prod_id"] = product_id
            context["prod_name"] = product_name
            context["prod_r1"] = product_rate1
            context["prod_r2"] = product_rate2
            context["prod_r3"] = product_rate3

    if 'prod_name' in request.POST and 'product-form-submitted' not in request.POST:
        product_name = request.POST['prod_name']
        product_query = Menu.objects.filter(product_name__exact=product_name)
        context['product_id'] = product_query[0].product_ID
        context['product_name'] = product_name
        context['product_selected'] = True
        request.session['prod_name'] = context['product_name']
        try:
            context['product_qty'] = request.POST['prod_qty']
        except MultiValueDictKeyError:
            pass
        try:
            context['product_qlt'] = request.POST['prod_qlt']
        except MultiValueDictKeyError:
            pass

        try:
            context['prod_list'] = request.session['prod_list']
        except:
            pass

    if 'product-form-submitted' in request.POST:
        try:
            if request.POST['prod_name'] == '' or request.POST['prod_qty'] == '' or request.POST['prod_qlt'] == '':
                context['incomplete_form'] = True
                context['product_qty'] = request.POST['prod_qty']
                context['product_qlt'] = request.POST['prod_qlt']
                product_name = request.POST['prod_name']
                product_query = Menu.objects.filter(product_name__exact=product_name)
                context['product_id'] = product_query[0].product_ID
                context['product_name'] = product_name
                try:
                    context['prod_list'] = request.session['prod_list']
                except:
                    pass


            else:

                context['incomplete_form'] = False
                prod_qlt = request.POST['prod_qlt']
                product_name = request.session['prod_name']
                product_query = Menu.objects.filter(product_name__exact=product_name)
                if prod_qlt == 'a1':
                    context['product_price'] = product_query[0].product_rate_1
                elif prod_qlt == 'a2':
                    context['product_price'] = product_query[0].product_rate_2
                else:
                    context['product_price'] = product_query[0].product_rate_3
                try:
                    check = request.session['prod_list']

                except KeyError:
                    request.session['prod_list'] = []

                prod_list = []
                no_of_prods = len(request.session['prod_list'])
                prod_list.append(no_of_prods + 1)
                prod_list.append(request.session['prod_name'])
                prod_list.append(context['product_price'])
                prod_list.append(request.POST['prod_qty'])
                prod_list.append(int(request.POST['prod_qty']) * int(context['product_price']))
                request.session['prod_list'].append(prod_list)
                context['prod_list'] = request.session['prod_list']
                request.session['prod_list_created'] = True
                context['product_qlt'] = ''
                context['product_qty'] = ''

        except MultiValueDictKeyError:
            pass

        try:
            context['product_qty'] = request.POST['prod_qty']
            try:
                context['prod_list'] = request.session['prod_list']
            except:
                pass

        except MultiValueDictKeyError:
            pass

        try:
            context['product_qlt'] = request.POST['prod_qlt']
            try:
                context['prod_list'] = request.session['prod_list']
            except:
                pass

        except MultiValueDictKeyError:
            pass
    try:
        if '-' in list(request.POST.values()):
            x = list(request.POST.keys())
            x = x[1]
            x = x.split('-')
            x = int(x[1]) - 1
            prod_list = request.session['prod_list']
            print(x)
            prod_list.pop(x)
            for i in prod_list:
                if i[0] > (x + 1):
                    i[0] = i[0] - 1
            request.session['prod_list'] = prod_list
            context['prod_list'] = request.session['prod_list']
    except IndexError:
        pass
    try:
        for m in context['prod_list']:
            total += int(m[4])
        context['total']=total
        output = calculate_discount(total,context['cust_id']!='Guest')
        print(total)
        print(context['cust_id']!='Guest')
        print(output)
        if output:
            context['discount'] = output['discount']
            context['total_amount'] = output['total_amount']
    except KeyError:
        context['prod_list'] = []

    if 'cancel' in request.POST:
        try:
            context['cust_name'] = ''
            context['cust_id'] = ''
            request.session['ph_no'] = ''
            context['ph_no'] = ''
            context['logged'] = False
            request.session['prod_list'] = []
            context['prod_list'] = request.session['prod_list']
        except:
            pass
    context["date"] = f"{datetime.datetime.now():%Y-%m-%d}"
    n = random.randint(1000, 9999)
    context["invoice_num"] = str(n)
    print(context)
    return render(request, "invoice.html", context=context)
import datetime
import random

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from .models import Menu, Customers
from .utils import getmenu, getcustomer, calculate_discount


# Create your views here.
def refresh_data():
    Menu.objects.all().delete()
    Customers.objects.all().delete()

    menu_dict = getmenu()

    for i in menu_dict:
        product_ID = i
        product_name = menu_dict[i][0]
        product_rate_1 = menu_dict[i][1]
        product_rate_2 = menu_dict[i][2]
        product_rate_3 = menu_dict[i][3]

        m = Menu.objects.create(product_ID=product_ID, product_name=product_name, product_rate_1=product_rate_1,
                                product_rate_2=product_rate_2,
                                product_rate_3=product_rate_3)
        m.save()

    customer_dict = getcustomer()

    for i in customer_dict:
        customer_id = i
        customer_name = customer_dict[i][0]
        customer_phone_no = customer_dict[i][1]

        m = Customers.objects.create(customer_ID=customer_id, customer_name=customer_name,
                                     customer_phone_no=customer_phone_no)

        m.save()


def home_view(request):
    context = {'logged': False}
    request.session['prod_list_created'] = True
    total = 0
    print(request.POST)

    try:
        cust_ph_no = request.POST['ph_number']
        customer_query = Customers.objects.filter(customer_phone_no__exact=cust_ph_no)
        context['cust_name'] = customer_query[0].customer_name
        context['cust_id'] = customer_query[0].customer_ID
        context['ph_no'] = cust_ph_no
        context['logged'] = True
        request.session['ph_no'] = request.POST['ph_number']
        request.session['guest'] = False
        request.session['prod_list'] = []

    except IndexError:
        cust_ph_no = request.POST['ph_number']
        context['cust_name'] = 'Guest'
        context['cust_id'] = 'Guest'
        context['ph_no'] = cust_ph_no
        context['logged'] = True
        request.session['ph_no'] = cust_ph_no
        request.session['guest'] = True
        request.session['prod_list'] = []

    except:
        pass

    if not context['logged']:
        try:
            if not request.session['guest']:
                cust_ph_no = request.session['ph_no']
                customer_query = Customers.objects.filter(customer_phone_no__exact=cust_ph_no)
                context['cust_name'] = customer_query[0].customer_name
                context['cust_id'] = customer_query[0].customer_ID
                context['ph_no'] = cust_ph_no
                context['logged'] = True

            else:
                context['ph_no'] = request.session['ph_no']
                context['cust_name'] = 'Guest'
                context['cust_id'] = 'Guest'
                context['logged'] = True


        except:
            pass

    if context['logged']:
        product_id = []
        product_name = []
        product_rate1 = []
        product_rate2 = []
        product_rate3 = []

        product_query = Menu.objects.all()
        for i in product_query:
            product_id.append(i.product_ID)
            product_name.append(i.product_name)
            product_rate1.append(i.product_rate_1)
            product_rate2.append(i.product_rate_2)
            product_rate3.append(i.product_rate_3)
            context["prod_id"] = product_id
            context["prod_name"] = product_name
            context["prod_r1"] = product_rate1
            context["prod_r2"] = product_rate2
            context["prod_r3"] = product_rate3

    if 'prod_name' in request.POST and 'product-form-submitted' not in request.POST:
        product_name = request.POST['prod_name']
        product_query = Menu.objects.filter(product_name__exact=product_name)
        context['product_id'] = product_query[0].product_ID
        context['product_name'] = product_name
        context['product_selected'] = True
        request.session['prod_name'] = context['product_name']
        try:
            context['product_qty'] = request.POST['prod_qty']
        except MultiValueDictKeyError:
            pass
        try:
            context['product_qlt'] = request.POST['prod_qlt']
        except MultiValueDictKeyError:
            pass

        try:
            context['prod_list'] = request.session['prod_list']
        except:
            pass

    if 'product-form-submitted' in request.POST:
        try:
            if request.POST['prod_name'] == '' or request.POST['prod_qty'] == '' or request.POST['prod_qlt'] == '':
                context['incomplete_form'] = True
                context['product_qty'] = request.POST['prod_qty']
                context['product_qlt'] = request.POST['prod_qlt']
                product_name = request.POST['prod_name']
                product_query = Menu.objects.filter(product_name__exact=product_name)
                context['product_id'] = product_query[0].product_ID
                context['product_name'] = product_name
                try:
                    context['prod_list'] = request.session['prod_list']
                except:
                    pass


            else:

                context['incomplete_form'] = False
                prod_qlt = request.POST['prod_qlt']
                product_name = request.session['prod_name']
                product_query = Menu.objects.filter(product_name__exact=product_name)
                if prod_qlt == 'a1':
                    context['product_price'] = product_query[0].product_rate_1
                elif prod_qlt == 'a2':
                    context['product_price'] = product_query[0].product_rate_2
                else:
                    context['product_price'] = product_query[0].product_rate_3
                try:
                    check = request.session['prod_list']

                except KeyError:
                    request.session['prod_list'] = []

                prod_list = []
                no_of_prods = len(request.session['prod_list'])
                prod_list.append(no_of_prods + 1)
                prod_list.append(request.session['prod_name'])
                prod_list.append(context['product_price'])
                prod_list.append(request.POST['prod_qty'])
                prod_list.append(int(request.POST['prod_qty']) * int(context['product_price']))
                request.session['prod_list'].append(prod_list)
                context['prod_list'] = request.session['prod_list']
                request.session['prod_list_created'] = True
                context['product_qlt'] = ''
                context['product_qty'] = ''

        except MultiValueDictKeyError:
            pass

        try:
            context['product_qty'] = request.POST['prod_qty']
            try:
                context['prod_list'] = request.session['prod_list']
            except:
                pass

        except MultiValueDictKeyError:
            pass

        try:
            context['product_qlt'] = request.POST['prod_qlt']
            try:
                context['prod_list'] = request.session['prod_list']
            except:
                pass

        except MultiValueDictKeyError:
            pass
    try:
        if '-' in list(request.POST.values()):
            x = list(request.POST.keys())
            x = x[1]
            x = x.split('-')
            x = int(x[1]) - 1
            prod_list = request.session['prod_list']
            print(x)
            prod_list.pop(x)
            for i in prod_list:
                if i[0] > (x + 1):
                    i[0] = i[0] - 1
            request.session['prod_list'] = prod_list
            context['prod_list'] = request.session['prod_list']
    except IndexError:
        pass
    try:
        for m in context['prod_list']:
            total += int(m[4])
        context['total']=total
        output = calculate_discount(total,context['cust_id']!='Guest')
        print(total)
        print(context['cust_id']!='Guest')
        print(output)
        if output:
            context['discount'] = output['discount']
            context['total_amount'] = output['total_amount']
    except KeyError:
        context['prod_list'] = []

    if 'cancel' in request.POST:
        try:
            context['cust_name'] = ''
            context['cust_id'] = ''
            request.session['ph_no'] = ''
            context['ph_no'] = ''
            context['logged'] = False
            request.session['prod_list'] = []
            context['prod_list'] = request.session['prod_list']
        except:
            pass
    context["date"] = f"{datetime.datetime.now():%Y-%m-%d}"
    n = random.randint(1000, 9999)
    context["invoice_num"] = str(n)
    if 'refresh' in request.POST:
        refresh_data()
    print(context)
    return render(request, "invoice.html", context=context)
