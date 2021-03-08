from proxy.scripts.members import get_member, get_members, search_member
from proxy.scripts.document import get_html_document, get_json_document, get_member_documents
from proxy.scripts.decisions import get_decisions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request


# Create your views here.


class DecisionsView(APIView):
    def get(self, request: Request):
        decisions = get_decisions(request.query_params)
        return Response(decisions)


class MemberSearchView(APIView):
    def get(self, request: Request):
        members = search_member(request.query_params)
        return members


class MembersView(APIView):
    def get(self, request: Request):
        members = get_members(request.query_params)
        return Response(members)


class MemberView(APIView):
    def get(self, request: Request, id):
        member = get_member(id)
        return Response(member)


class MemberDocumentsView(APIView):
    def get(self, request: Request, id):
        decisions = get_member_documents(id, request.query_params)
        return Response(decisions)


class JSONDocumentView(APIView):
    def get(self, request: Request, id):
        decisions = get_json_document(id)
        return Response(decisions)


class HTMLDocumentView(APIView):
    def get(self, request: Request, id):
        decisions = get_html_document(id)
        return Response(decisions)
