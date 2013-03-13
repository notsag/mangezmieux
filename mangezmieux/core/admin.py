from models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from auth.models import *

class ProfilUtilisateurInline(admin.StackedInline):
    """ As you are noticed your profile will be edited as inline form """
    model = ProfilUtilisateur
    can_delete = False
 
class UserAdmin(OriginalUserAdmin):
    """ Just add inlines to the original UserAdmin class """
    inlines = [ProfilUtilisateurInline, ]
    
admin.site.register(Recette)
admin.site.register(Produit)
admin.site.register(LigneRecette)
admin.site.register(TypeProduit)
admin.site.register(Unite)
admin.site.register(Categorie)
admin.site.register(Repas)
admin.site.register(LigneProduit)
admin.site.register(Tag)
admin.site.register(RecetteFavorite)

try:
    admin.site.unregister(User)
finally:
    admin.site.register(User, UserAdmin)

