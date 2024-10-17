from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .models import Server
from django.db.models import Count

from .schema import server_list_docs


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
            List and filter Server objects based on query parameters.

        Query Parameters:
            - category (str, optional): Filters servers by the specified category name.
            - by_user (str, optional): Filters servers where the current user is a member.
                                       Must be set to "true". Requires user authentication.
            - by_owner (str, optional): Filters servers where the current user is the owner.
                                        Requires user authentication.
            - qty (int, optional): Limits the number of servers returned to the specified quantity.
            - by_serverid (int, optional): Filters servers by the specified server ID.
                                           Requires user authentication. Raises a ValidationError if the ID is invalid or the server does not exist.
            - with_num_members (str, optional): If provided, includes the number of members in each server.
                                                The value of this parameter controls the presence of the "num_members" field in the serialized response.

        Exceptions:
            - AuthenticationFailed: Raised if `by_user` or `by_serverid` is provided but the user is not authenticated.
            - ValidationError: Raised if the `by_user` parameter is invalid or if the provided server ID (`by_serverid`) is invalid or does not exist.

        Returns:
            Response: A serialized list of Server objects, filtered and modified based on the query parameters.
        """

        category = request.query_params.get(
            "category"
        )  # gets the params after the = sign
        by_user = request.query_params.get("by_user") == "true"
        by_owner = request.query_params.get("by_owner") == "true"
        qty = request.query_params.get("qty")
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed(
                    "You must be logged in to view this content."
                )

        if by_owner:
            if by_owner and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(owner=user_id)
            else:
                raise AuthenticationFailed(
                    "You must be logged in to view this content."
                )

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed(
                    "You must be logged in to view this content."
                )
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        f"Server with id {by_serverid} does not exist."
                    )
            except ValueError:
                raise ValidationError(f"Server with id {by_serverid} does not exist.")

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
