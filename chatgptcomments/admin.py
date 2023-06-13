from django.contrib import admin
from chatgptcomments.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class CommentsResource(resources.ModelResource):
    class Meta:
        model = Comments
        export_order = (
            'url', 'content', 'publisher',
            'website_authentication',
            'number_of_comments',
            'number_of_shares',
            'number_of_likes',
            'source_platform'
        )


@admin.register(Comments)
class CommentsAdmin(ImportExportModelAdmin):
    list_display = (
        'url', 'content', 'publisher',
        'website_authentication',
        'number_of_comments',
        'number_of_shares',
        'number_of_likes',
        'source_platform'
    )
    search_fields = (
        'url', 'content', 'publisher',
        'website_authentication',
        'number_of_comments',
        'number_of_shares',
        'number_of_likes',
        'source_platform'
    )
    resource_class = CommentsResource


class CommentIndexResource(resources.ModelResource):
    class Meta:
        model = CommentIndex
        export_order = ('cmt_keyword', 'cmt_list')


@admin.register(CommentIndex)
class CommentIndexAdmin(ImportExportModelAdmin):
    list_display = ('cmt_keyword', 'cmt_list')
    search_fields = ('cmt_keyword',)
    resource_class = CommentIndexResource


class CmtViewRes(resources.ModelResource):
    class Meta:
        model = CommentView
        export_order = ('img_name', 'img_text')


@admin.register(CommentView)
class CmtVieAdmin(ImportExportModelAdmin):
    list_display = ('img_name', 'img_text')
    search_fields = ('img_name',)
    resource_class = CmtViewRes


class QAIndexResource(resources.ModelResource):
    class Meta:
        model = QAIndex
        export_order = ('keyword', 'ids')


@admin.register(QAIndex)
class QAIndexAdmin(ImportExportModelAdmin):
    list_display = ('keyword', 'ids')
    search_fields = ('keyword',)
    resource_class = QAIndexResource


class QAmapRes(resources.ModelResource):
    class Meta:
        model = QAmap
        export_order = ('question', 'answer')


@admin.register(QAmap)
class QAmapAdmin(ImportExportModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('question',)
    resource_class = QAmapRes
