from proxy.scripts.members import get_member, get_members, search_member
from proxy.scripts.document import get_html_document, get_json_document, get_member_documents
from proxy.scripts.decisions import get_decisions
from proxy.scripts.votes import get_votes
from proxy.scripts.vote import get_vote
from proxy.scripts.parties import get_party
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request


# Create your views here.

""" Decisions """


class DecisionsView(APIView):
    def get(self, request: Request):
        decisions = get_decisions(request.query_params)
        return Response(decisions)


""" Members """


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


""" Documents """


class JSONDocumentView(APIView):
    def get(self, request: Request, id):
        decisions = get_json_document(id)
        return Response(decisions)


class HTMLDocumentView(APIView):
    def get(self, request: Request, id):
        decisions = get_html_document(id)
        return Response(decisions)


""" Parties """


class PartyView(APIView):
    def get(self, request: Request, party: str):
        party_data = get_party(party.lower())
        return Response(party_data)


""" Votes """


class VotesView(APIView):
    def get(self, request: Request):
        votes = get_votes(request.query_params)
        return Response(votes)


class VoteView(APIView):
    def get(self, request: Request, id: str, proposition: int):
        vote = get_vote(id, proposition)
        return Response(vote)
