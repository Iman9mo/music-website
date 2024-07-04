from django.contrib import admin
from .models import Category, Artist, Song, Comment, Action

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('user', 'content', 'approved', 'created_at')
    can_delete = False

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'user', 'likes', 'views', 'approved')
    list_filter = ('approved', 'category', 'artist')
    search_fields = ('title', 'artist__name', 'category__name', 'user__username')
    actions = ['approve_songs', 'block_songs']
    inlines = [CommentInline]

    def approve_songs(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected songs have been approved.")
    approve_songs.short_description = "Approve selected songs"

    def block_songs(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected songs have been blocked.")
    block_songs.short_description = "Block selected songs"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'song', 'user', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('content', 'song__title', 'user__username')
    actions = ['approve_comments', 'block_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected comments have been approved.")
    approve_comments.short_description = "Approve selected comments"

    def block_comments(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected comments have been blocked.")
    block_comments.short_description = "Block selected comments"

class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'action_type', 'timestamp')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('user__username', 'song__title', 'action_type')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Action, ActionAdmin)
