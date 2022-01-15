from .models import *
from django.shortcuts import render
import razorpay
from .forms import *

from blog.models import *
# from project.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRECT_KEY
# Create your views here.
# client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRECT_KEY))
def payment(request,requirement_id):
    requirement=Requiremt.objects.get(id=requirement_id)
    print(requirement.message)
    amount=int(requirement.message)
    if request.method == "POST":
        name = request.POST.get('name')
        requirement=Requiremt.objects.get(id=requirement_id)
        print(requirement.message)
        amount=int(requirement.message)
        # amount = int(request.POST.get('amount')) * 100
        # property_type=request.POST.get('property_type')
        amount=amount*100
        client = razorpay.Client(auth=('rzp_test_48Z9LMTDVAN5JU', 'gMxfhwgZ73ANYJQCeblLMy7W'))
        response_payment = client.order.create(dict(amount=amount,
                                                    currency='INR')
                                               )

        order_id = response_payment['id']
        order_status = response_payment['status']

        if order_status == 'created':
            payment = Payment(
                name=name,
                amount=amount*100,
                # property_type=property_type,
                order_id=order_id
            )
          
        payment.save()
        requirement=Requiremt.objects.update_or_create(id=requirement_id,
        defaults={'paid':True}
        )
        response_payment['name'] = name

        form = PaymentForm(request.POST or None)
        return render(request, 'payment.html', {'form': form, 'payment': response_payment})

    form = PaymentForm()
    return render(request, 'payment.html', {'form': form})


def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_48Z9LMTDVAN5JU', 'gMxfhwgZ73ANYJQCeblLMy7W'))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id = response['razorpay_payment_id']
        payment.paid = True
        payment.save()
        
        return render(request, 'payment_status.html', {'status': True,'payment_id':payment.payment_id})
    except:
        return render(request, 'payment_status.html', {'status': False})

    # order_amount = 30000
    # order_currency = 'INR'
    # # order_receipt = 'order_rcptid_11'
    # # notes = {'Shipping address': 'Bommanahalli, Bangalore'}   # OPTIONAL

    # payment_order=client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture=1))
    # payment_order_id=payment_order['id']
    # amount={
    #     'amount':300,'api_key':RAZORPAY_API_KEY,'order_id':payment_order_id
    # }
    return render(request,'payment.html',amount)


