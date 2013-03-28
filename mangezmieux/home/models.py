#-*- coding:utf-8 -*-
from django.db import models

class News(models.Model):
	"""
	Infos concernant le site qui peuvent être postées sur la home page 
	"""
	nom = models.CharField(max_length=50)
	info = models.TextField()
	date_pub = models.DateField(auto_now=True)
	
	def __unicode__(self):
		return self.nom

