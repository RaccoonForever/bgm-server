"""
Script that will handle different Namespaces
"""
from flask_restplus import Namespace

class KingDominoNamespace:
    api = Namespace("KingDomino-AI", description="Kingdomino API operations")
