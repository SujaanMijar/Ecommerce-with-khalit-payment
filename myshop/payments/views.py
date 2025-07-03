from django.shortcuts import render,redirect,get_object_or_404
import requests
import json
from core.models import Order
import uuid
from django.http import JsonResponse
from .models import Transaction
# Create your views here.
def initkhalti(request,id):
    data=Order.objects.get(id=id)
    total=data.total
    url = "https://dev.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps({
        "return_url":"http://127.0.0.1:8000/payment/verify",
        "website_url": "https://example.com/",
        "amount": int(float(total)) * 100,
        "purchase_order_id": data.id,
        "purchase_order_name": data.product,
        "customer_info": {
        "name": request.user.username,
        "email": request.user.email,
        "phone": request.user.phone
        }
    })
    headers = {
        'Authorization': 'key 5991ed2d3b7948238c2830d141ca8a7d',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    payments_url=json.loads(response.text)['payment_url']
    return redirect(payments_url)

def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key 5991ed2d3b7948238c2830d141ca8a7d',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        purchase_order_id = request.GET.get('purchase_order_id')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            order=get_object_or_404(Order,id=purchase_order_id)
            order.is_pay=True
            order.save()
            Transaction.objects.create(order=order,user=request.user,amount=new_res
            ['total_amount'],transaction_id=transaction_id)
           

           
            return redirect('my_order')
        else:
            print("Payment verification failed. Khalti response:", json.dumps(new_res, indent=4))
            return JsonResponse({'error': 'Payment verification failed'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)