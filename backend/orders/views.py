from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Order
from.serializers import *
import os
from dotenv import load_dotenv
load_dotenv()
import uuid
import requests
from rest_framework.response import Response
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import json
from django.contrib.auth.models import User
from .models import OrderStatus
from rest_framework import status
# Create your views here.
class OrderViewSet(ModelViewSet):
     serializer_class = OrderSerializer
     queryset = Order.objects.all()

from django.db import transaction
from django.db.utils import IntegrityError

class InitiateKhaltiPayment(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Start a database transaction
        try:
            with transaction.atomic():
                serializer = KhaltiPaymentSerializer(data=request.data)
                if serializer.is_valid():
                    return_url = serializer.validated_data["return_url"]
                    website_url = serializer.validated_data["website_url"]
                    price = serializer.validated_data["price"]
                    quantity = serializer.validated_data["quantity"]
                    name = serializer.validated_data["name"]
                    image_url = serializer.validated_data.get("image_url", "")
                    user_id = serializer.validated_data["user_id"]
                    phone_number = serializer.validated_data["phone_number"]
                    user = User.objects.get(id=user_id)

                    # Create order (if any step fails, everything will be rolled back)
                    order = Order.objects.create(
                        user=user,
                        name=name,
                        price=price,
                        quantity=quantity,
                        image_url=image_url,
                    )

                    payload = json.dumps({
                        "return_url": return_url,
                        "website_url": website_url,
                        "amount": float(price),
                        "purchase_order_id": str(order.id),
                        "purchase_order_name": order.name,
                        "customer_info": {
                            "name": "test",
                            "email": 'test@gmail.com',
                            "phone": phone_number
                        }
                    })

                    # Request to Khalti API
                    headers = {
                        'Authorization': f"key {os.environ.get('KHALTI_SECRET_KEY')}",
                        'Content-Type': 'application/json',
                    }

                    response = requests.post("https://a.khalti.com/api/v2/epayment/initiate/", headers=headers, data=payload)
                    print("response==",response)
                    new_res = response.json()
                    
                    # If request is successful, return redirect URL
                    return Response({'redirect_url': new_res['payment_url'],'order_id':order.id}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("internal server error",e)
            # Handle the error and rollback
            return Response({'error': 'An error occurred while processing the order.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Handle any other errors and rollback
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VerifyKhalti(APIView):
    permission_classes = [AllowAny]
    def get(self,request,*args,**kwargs):
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        if request.method == 'GET':
            headers = {
                'Authorization': f"key {os.environ.get('KHALTI_SECRET_KEY')}",
                'Content-Type': 'application/json',
            }
            pidx = request.GET.get('pidx')
            purchase_order_id = kwargs.get('purchase_order_id')
            print("cat__id=====",purchase_order_id)
            data = json.dumps({
                'pidx':pidx
            })
            res = requests.request('POST',url,headers=headers,data=data)
            print(res)
            print(res.text)

            new_res = json.loads(res.text)
            print(new_res)

            if new_res['status'] == 'Completed':
                
                    order = Order.objects.get(id=self.request.GET.get('purchase_order_id'))
                    print("order",order)
                    if not order:
                       return Response({'data':{'message':'Order could not be completed. Please contact administration.'}},status=status.HTTP_400_BAD_REQUEST)
                    order.order_status = OrderStatus.COMPLETED
                    order.save()
                    return Response({'data':{'message':'Order Created'}},status=status.HTTP_200_OK)
                   
            #  Update status based on khalti response and notify user      
            
            # elif new_res['status'] == 'Pending':
            #     try:
            #         category = Order.objects.get(id=cat_id)
            #         Upgrade.objects.create(user=self.request.user,category=category,payment_status=new_res['status'])
            #     except Exception as e:
            #         return Response({'data':{'message':'Url modified'}},status=status.HTTP_400_BAD_REQUEST)


            # elif new_res['status'] == 'Expired':
            #     return Response({'data':{'message':'Pidx expired'}},status=status.HTTP_400_BAD_REQUEST)
            # elif new_res['status'] == 'Initiated':
                
            #     return Response({'data':{'message':'Payment didnot succed.Please contace support center.'}},status=status.HTTP_400_BAD_REQUEST)
            # elif new_res['status'] == 'Refunded':
                
            #     return Response({'data':{'message':'Payment refunded.'}},status=status.HTTP_400_BAD_REQUEST)
            # elif new_res['status'] == 'User canceled':
                
            #     return Response({'data':{'message':'User cancelled payment request'}},status=status.HTTP_400_BAD_REQUEST)
            # elif new_res['status'] == 'Partially Refunded':
                
            #     return Response({'data':{'message':'Payment partially refunded'}},status=status.HTTP_400_BAD_REQUEST)
            else:
                
                return Response({'data':{'message':'Payment didnot succed.Please contace support center.'}},status=status.HTTP_400_BAD_REQUEST)

            return redirect(os.environ.get('FRONTEND_BASE_URL'))