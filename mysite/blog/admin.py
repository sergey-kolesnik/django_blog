from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Класс для управления постами в админке Django.
    
    Атрибуты:
        list_display (list[str]): Список полей, отображаемых в списке записей.
        list_filter (list[str]): Список фильтров для поиска записей.
        search_fields (list[str]): Поля, по которым осуществляется поиск.
        prepopulated_fields (dict[str, tuple[str]]): Автоматическое заполнение поля slug значением title.
        raw_id_fields (list[str]): Поле author будет представлено в виде сырого ID.
        date_hierarchy (str): Поле для иерархии дат.
        ordering (list[str]): Порядок сортировки записей.
        show_facets (int): Всегда показывать фасеты.
    """
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    show_facets = admin.ShowFacets.ALWAYS
