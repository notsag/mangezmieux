PROJECT=mangezmieux
PKGDIR=debian/$(PROJECT)
CODEDIR=$(PKGDIR)/usr/share
APACHECONF=$(PKGDIR)/etc/apache2/sites-available
STATICDIR=$(PKGDIR)/var/www/mangezmieux
STATICS=statics

install:
	find $(PROJECT) -name "*.pyc" -delete
	mkdir -p $(CODEDIR)
	cp -r $(PROJECT) $(CODEDIR)/
	rm -rf $(CODEDIR)/$(PROJECT)/static
	mkdir -p $(APACHECONF)
	cp mangezmieux.virtualhost $(APACHECONF)/mangezmieux
	mkdir -p $(STATICDIR)
	cp -r $(PROJECT)/static/* $(STATICS)/
	cp -r $(STATICS) $(STATICDIR)
clean:
	find debian/ -maxdepth 1 ! -name "*templates" -a ! -name "*config" -a ! -name "*control" -a ! -name "*rules" -a ! -name "debian" -a ! -name "*changelog" -a ! -name "*compat" -a ! -name "*copyright" -a ! -name "*postinst" -exec rm -rf {} \;
	find statics/ -maxdepth 1 ! -name "statics" -a ! -name "*admin" -a ! -name "*rest_framework" -exec rm -rf {} \;

