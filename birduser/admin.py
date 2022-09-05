
from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
import admin_thumbnails

# Register your models here.
class userAdmin(admin.StackedInline):
    model = User
class addressAdmin(admin.StackedInline):
    model = address
    list_display = ['id', 'phoneNumber', 'area','postalCode', 'address1', 'address2']
class profileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','nickname','image_display', 'address_display']
    readonly_fields= ('avatar', 'address')
    @admin.display(description='Avatar')
    def image_display(self, object):
        return mark_safe('<img src = "{}" width="100px"/>'.format(object.avatar.url))

    @admin.display(description='address')
    def address_display(self, object):
        return mark_safe('<p>{}</p><p>{}</p><p>{}</p><p>{}</p>'.format(address.objects.get(id = object.address.id).phoneNumber,
                                                                            address.objects.get(id = object.address.id).area,
                                                                            address.objects.get(id = object.address.id).address1,
                                                                            address.objects.get(id = object.address.id).address2               
                                                                                        ))
admin.site.register(userprofile,profileAdmin)

@admin_thumbnails.thumbnail('pict')
class pictureAdmin(admin.StackedInline):  
    model = rescueBirdPicture
class rescueRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'rescueRequester','resuceDescription','requestTime', 'progress', 'address_display']
    inlines = [pictureAdmin]
    @admin.display(description='address')
    def address_display(self, object):
        return mark_safe('<p>{}</p><p>{}</p><p>{}</p><p>{}</p>'.format(address.objects.get(id = object.address.id).phoneNumber,
                                                                            address.objects.get(id = object.address.id).area,
                                                                            address.objects.get(id = object.address.id).address1,
                                                                            address.objects.get(id = object.address.id).address2               
                                                                                        ))
# @admin_thumbnails.thumbnail('pict')
# class birdPictureAdmin(admin.ModelAdmin):
#     list_display = ['id', 'bird', 'image_display']
#     readonly_fields= ('bird', )
#     def image_display(self, object):
#         return mark_safe('<img src = "{}" width="100px"/>'.format(object.pict.url))
# admin.site.register(birdPicture, birdPictureAdmin)


class petAdoptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'requester', 'adopter','progress', 'time']
    readonly_fields= ('requester', )
    def bird_display(self, obj):
        return mark_safe('<p>Name: {}</p><p>Species: {}</p><p>Age: {}</p>'.format(bird.objects.get(obj.birds.id).name, 
                                                                        bird.objects.get(obj.birds.id).species,
                                                                        bird.objects.get(obj.birds.id).age                           
                                                                                                            ))
admin.site.register(petAdoption,petAdoptionAdmin)
@admin_thumbnails.thumbnail('pict')
class birdPictureInline(admin.StackedInline):
    model = birdPicture
    def imageDisplay(self, obj):
        return mark_safe('<img src = "{}" width="100px"/>'.format(obj.pict.url))
class petAdoptionInline(admin.StackedInline):
    model = petAdoption
class birdAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'species', 'age', 'adoptDescription']
    inlines = [birdPictureInline,petAdoptionInline,]
    @admin.display(ordering='-id',)
    def address_display(self, object):
        return mark_safe('<p>{}</p><p>{}</p><p>{}</p><p>{}</p>'.format(address.objects.get(id = object.address.id).phoneNumber,
                                                                            address.objects.get(id = object.address.id).area,
                                                                            address.objects.get(id = object.address.id).address1,
                                                                            address.objects.get(id = object.address.id).address2               
                                                                                        ))
admin.site.register(rescueRequest,rescueRequestAdmin)

class anonymousRequestAdmin(admin.ModelAdmin):
    list_display = ['id','rescueRequester', 'resuceDescription', 'requestTime']
    readonly_fields= ('rescueRequester', )
admin.site.register(anonymousRequest, anonymousRequestAdmin)

class anonymousRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'rescueRequester', 'resuceDescription', 'requestTime']
    inlines = [pictureAdmin, ]



class anonymousRequestInline(admin.StackedInline):
    model = anonymousRequest
class anonymousProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'address_display']
    inlines = [anonymousRequestInline]
    @admin.display(ordering='-id',)
    def address_display(self, object):
        return mark_safe('<p>{}</p><p>{}</p><p>{}</p><p>{}</p>'.format(address.objects.get(id = object.address.id).phoneNumber,
                                                                            address.objects.get(id = object.address.id).area,
                                                                            address.objects.get(id = object.address.id).address1,
                                                                            address.objects.get(id = object.address.id).address2               
                                                                                        ))
admin.site.register(anonymousProfile, anonymousProfileAdmin)


class userDonationRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'transitionTime', 'amount', 'success']
admin.site.register(userDonationRecord,userDonationRecordAdmin)



admin.site.register(bird, birdAdmin)
