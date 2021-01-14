from django.contrib import admin

from .models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "text", "author", "score", "pub_date",)
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class ReviewAdminComment(admin.ModelAdmin):
    list_display = ("pk", "author", "text", "pub_date", "review",)
    search_fields = ("review", "author", "text")
    list_filter = ("author", "pub_date")


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, ReviewAdminComment)
