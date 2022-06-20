from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from listings import models as list_models
from listings import serializers as list_serializers
from agents import models as agent_models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from payments import serializers as pay_serializers
from payments import models as pay_models
from properties import models as prop_models
from django.http.request import QueryDict

from myhome.strings import *
from rest_framework.parsers import MultiPartParser, FormParser


class ListingModeListView(generics.ListAPIView):
    queryset = list_models.ListingMode.objects.all()
    serializer_class = list_serializers.ListingModeSerializer
    # permission_classes = [IsAuthenticated,]


class ListingTypeListView(generics.ListAPIView):
    queryset = list_models.ListingType.objects.all()
    serializer_class = list_serializers.ListingTypeSerializer
    # permission_classes = [IsAuthenticated,]


class ListingStateListView(generics.ListAPIView):
    queryset = list_models.ListingState.objects.all()
    serializer_class = list_serializers.ListingStateSerializer
    # permission_classes = [IsAuthenticated,]


class AgentNumberOfListingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, **kwargs):
        user = self.request.user
        try:
            currentAgentAdmin = agent_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            return None
        
        agent_listing_count = list_models.MainListing.objects.filter(agent=currentAgentAdmin.agent).count()

        return Response(data=agent_listing_count, status=status.HTTP_200_OK)


class ListingListCreateView(generics.ListCreateAPIView):
    queryset = list_models.MainListing.objects.all()
    serializer_class = list_serializers.MainListingSerializer
    permission_classes = [IsAuthenticated,]
    parser_clasess = [MultiPartParser, FormParser]

    def post(self, request, **kwargs):
        
        pm_key = request.data.get("payment[pm_key]")

        #==================MAIN LISTING==========================================================

        main_listing = {}

        main_listing["listing_type"] = request.data.get("main_listing[listing_type]")
        main_listing["property_price"] = request.data.get("main_listing[property_price]")
        main_listing["currency"] = request.data.get("main_listing[currency]")
        main_listing["deposit_in_months"] = request.data.get("main_listing[deposit_in_months]")
        main_listing["property"] = request.data.get("main_listing[property]")
        main_listing["sub_property"] = request.data.get("main_listing[sub_property]")
        main_listing["agent"] = request.data.get("main_listing[agent]")

        if pm_key == PM_CASH_PAYMENT or pm_key == PM_BANK_TRANSFER or pm_key == PM_MOBILE_PAYMENT:
             main_listing["listing_state"] = "INACTIVE"
             main_listing["is_approved"] = False
        else:
             main_listing["listing_state"] = "ACTIVE"
             main_listing["is_approved"] = True

        if pm_key == PM_SUBSCRIPTION:
            main_listing["listing_mode"] = "SUBSCRIPTION"
        else:
            main_listing["listing_mode"] = "PAY_PER_LISTING"
        

        main_listing_querydict = QueryDict("", mutable=True)
        main_listing_querydict.update(main_listing)
        main_listing_serializer = self.get_serializer(data=main_listing_querydict)

        if main_listing_serializer.is_valid():
            # print("MAIN LISTING: YAYYYYYY! MAIN LISTING IS VALID")
            main_listing_instance = main_listing_serializer.save()
        else:
            print("Main listing has invalid data!")
            return Response(data="Main listing has ivalid data!", status=status.HTTP_400_BAD_REQUEST)

        #=================SUB LISTING============================================================
        cat_key = request.data.get("main_listing[cat_key]")
        sub_property_id = request.data.get("main_listing[sub_property]")

        try:
            villa_instance = prop_models.Villa.objects.get(id=sub_property_id)
        except:
            print(f"Villa {sub_property_id} not found!")
            return Response(data=f"Villa {sub_property_id} not found!", status=status.HTTP_404_NOT_FOUND)

        if cat_key == VILLA_KEY:
            print("VILLA SAVED!!!!!!!!!")
            list_models.VillaListing.objects.create(villa=villa_instance, main_listing=main_listing_instance)
       

        #==================COUPON================================================================
        coupon_payment_instance = None

        use_coupon = request.data.get("payment[coupon][use_coupon_payment]")
        listing_price = float(request.data.get("payment[listing_price]"))
        
        if use_coupon:
            coupon_code = request.data.get("payment[coupon][coupon_code]")
            try:
                coupon_instance = pay_models.Coupon.objects.get(code=coupon_code)
            except ObjectDoesNotExist:
                print(f"Coupon {coupon_code} not found!")
                return Response(data=f"Coupon {coupon_code} not found!", status=status.HTTP_404_NOT_FOUND)
            paid_amount = None
            try:
                if coupon_instance.current_value >= listing_price:
                    
                    paid_amount = listing_price
                else:
                    paid_amount = coupon_instance.current_value
                coupon_payment_instance = pay_models.CouponPayment.objects.create(coupon=coupon_instance, paid_amount=paid_amount)
                print("YOOOOOOOOO!!!!!: ",coupon_instance.current_value - paid_amount)
                pay_models.Coupon.objects.filter(code=coupon_code).update(current_value=coupon_instance.current_value - paid_amount)
                print("COUPON SAVED!!!!!!!!!")

            except:
                print(f"Something went wrong during saving coupon payment!")
                return Response(data=f"Something went wrong during saving coupon payment!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
        #==================PAYMENT================================================================

        payment = {}

        payment["payment_method"] = request.data.get("payment[payment_method]")
        payment["total_price"] = float(listing_price)
        payment["coupon_payment"] = coupon_payment_instance.id
        if pm_key == PM_CASH_PAYMENT or pm_key == PM_BANK_TRANSFER or pm_key == PM_MOBILE_PAYMENT:
             payment["is_approved"] = False
        else:
             payment["is_approved"] = True
        payment["narrative"] = request.data.get("payment[narrative]")

        payment_querydict = QueryDict("", mutable=True)
        payment_querydict.update(payment)

        payment_serializer = pay_serializers.PaymentSerializer(data=payment_querydict)
        if payment_serializer.is_valid():
            payment_instance = payment_serializer.save()
            print("PAYMENT SAVED!!!!!!!!!")
        else:
            print("Payment data is not valid!")
            return Response(data="Payment data is not valid!", status=status.HTTP_400_BAD_REQUEST)
    
        sub_payment_data = {}

        if pm_key == PM_BANK_TRANSFER:
            sub_payment_data["bank_name"] = request.data.get("payment[bank_transfer][bank_name]")
            sub_payment_data["bank_branch_name"] = request.data.get("payment[bank_transfer][bank_branch_name]")
            sub_payment_data["transaction_ref_number"] = request.data.get("payment[bank_transfer][transaction_ref_number]")
            sub_payment_data["payment_date"] = request.data.get("payment[bank_transfer][payment_date]")
            sub_payment_data["bank_full_address"] = request.data.get("payment[bank_transfer][bank_full_address]")


            bank_transfer_queridict = QueryDict("", mutable=True)
            bank_transfer_queridict.update(sub_payment_data)
            bank_transfer_serializer = pay_serializers.BankPaymentCreatBasicSerializer(data=bank_transfer_queridict)
            if bank_transfer_serializer.is_valid():
                # print("BANK: YAYYYYYY! BANK IS VALID")
                bank_transfer_instance = bank_transfer_serializer.save(payment=payment_instance)
                print("BANK TRANSFER SAVED!!!!!!!!!")

            else:
                print("Bank Payment data is not valid!")
                return Response(data="Bank Payment data is not valid!", status=status.HTTP_400_BAD_REQUEST)


        if pm_key == PM_BANK_TRANSFER or pm_key == PM_MOBILE_PAYMENT:
            reciepts = request.data.getlist("reciept")

            
            for reciept in reciepts:
                sub_payment = {"reciept": reciept}
                sub_payment_querydict = QueryDict("", mutable=True)
                sub_payment_querydict.update(sub_payment)

                sub_payment_serializer = None
                if pm_key == PM_BANK_TRANSFER:
                    sub_payment_serializer = pay_serializers.BankRecieptCreateBasicSerializer(data=sub_payment_querydict)
                    
                else:
                    print("Bank Reciept is not valid!")
                    return Response(data="Bank Reciept is not valid!", status=status.HTTP_400_BAD_REQUEST)



                if sub_payment_serializer.is_valid():
                    sub_payment_serializer.save(bank_payment=bank_transfer_instance)
                    print("Bank Reciept Saved!")
                else:
                    print("Sub-payment data is not valid!")
                    return Response(data="Sub-payment data is not valid!", status=status.HTTP_400_BAD_REQUEST)

        
        
        # print("LISTING DATA: ", request.data)
        
        
        # for file in reciept:
        #     print("FILE DATA: ", file)

        return Response(data=main_listing_serializer.data, status=status.HTTP_201_CREATED)
