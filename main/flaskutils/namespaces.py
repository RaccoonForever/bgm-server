"""
Script that will handle different Namespace for the entire application
"""
from flask_restplus import Namespace

class KingDominoNamespace:
    """
    KingDomino V1 Namespace class
    """
    api = Namespace('kingdomino', description="KingDomino API operations")