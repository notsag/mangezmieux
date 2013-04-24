from models import *
from auth.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin

class ProfilUtilisateurInline(admin.StackedInline):
    """ As you are noticed your profile will be edited as inline form """
    model = ProfilUtilisateur
    can_delete = False
 
class UserAdmin(OriginalUserAdmin):
    """ Just add inlines to the original UserAdmin class """
    inlines = [ProfilUtilisateurInline, ]
    
admin.site.register(Recette)
admin.site.register(Produit)
admin.site.register(ValeurNutritionnelle)
admin.site.register(LigneRecette)
admin.site.register(TypeProduit)
admin.site.register(Unite)
admin.site.register(Categorie)
admin.site.register(Repas)
admin.site.register(LigneProduit)
admin.site.register(Tag)
admin.site.register(RecetteFavorite)
admin.site.register(News)
admin.site.register(Panier)
admin.site.register(LignePanier)
admin.site.register(Commande)
admin.site.register(LigneCommande)
admin.site.register(Conversion)

try:
    admin.site.unregister(User)
finally:
    admin.site.register(User, UserAdmin)

