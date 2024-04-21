from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.template.loader import get_template
from django.utils import timezone
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from account.serializers import AccountSerializer, AccountCreateSerializer
from rest_framework.decorators import api_view, permission_classes
from core.utils.sendEmail import send_email

User = get_user_model()


# Admin View
@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAdminUser])
def user_route(req):
    paginator = PageNumberPagination()
    paginator.page_size = 20

    if req.method == "POST":
        _id = req.data["id"]
        del req.data["id"]

        print(req.data)
        user = User.objects.get(pk=_id, email=req.data["email"])
        user.first_name = req.data["first_name"]
        user.last_name = req.data["last_name"]
        user.is_active = req.data["is_active"]
        user.is_superuser = req.data["is_superuser"]
        user.save()
        print(user.is_superuser)
        return Response({})

        # return Response(data={},status=404)
    elif req.method == "DELETE":
        pass
    elif req.method == "GET":
        user = User.objects.all().exclude(is_superuser=True)
        if "filter" in req.query_params:
            user = User.objects.filter(is_superuser=True)

        return paginator.get_paginated_response(
            AccountSerializer(paginator.paginate_queryset(user, req), many=True).data)

    return Response({})

    # 


# @api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_delete(req, _id):
    try:
        User.objects.filter(id=_id).delete()
        return Response(True)
    except:
        return Response(False)


# ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

# User View
class CreateAccount(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountCreateSerializer
    permission_classes = []


class ViewUpdateAccount(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    # TODO write permission class only owner can view and update their details
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
def password_recovery(req):
    reset_email = verify_email(req.data["email"])
    if reset_email is not None:
        user: User = User.objects.filter(email=reset_email)
        if len(user):
            email = urlsafe_base64_encode(force_bytes(user[0].email))
            time = urlsafe_base64_encode(force_bytes(user[0].last_login))
            html_email = get_template("email_template/password_reset.html").render(
                context={"email": email, "time": time, "user": user[0]}, request=req)

            send_email(html_email=html_email, to_email=reset_email,
                       email_from="No-reply <noreply@elclassicjewelryshop.com>", subject="Password Reset")
            return Response({'status': True})
    return Response({"message": "account Does not Exist"}, status == status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def password_reset_success(req, time, _id):
    try:
        remail = urlsafe_base64_decode(force_str(_id)).decode('utf-8')
        rtime = urlsafe_base64_decode(force_str(time)).decode("utf-8")
        if verify_email(email=remail):
            new = User.objects.get(email=remail, last_login=rtime)
            if new is not None:
                html_email = get_template("email_template/p_reset_success.html").render(context={"user": new},
                                                                                        request=req)
                # TODO validate password to be accurate
                new.set_password(req.data["password"])
                new.last_login = timezone.now()
                new.save()
                try:
                    send_email(html_email=html_email, to_email=remail, subject="Password Reset Successful",
                               email_from="No-reply <noreply@elclassicjewelryshop.com>")
                except:
                    pass

                return Response({"message": "Password Reset Successfully"})
            return Response({"message": "Please a Valid Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist as e:
        return Response({"message": "Link Expired"}, status=status.HTTP_400_BAD_REQUEST)
    except UnicodeDecodeError as e:
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


# ALL PURPOSE

@api_view(["GET"])
def verify_email(req, email):
    result = False
    user: User = User.objects.filter(email=email)
    if len(user) > 0:
        result = True
        return Response({"result": result})

    return Response({"result": result})
