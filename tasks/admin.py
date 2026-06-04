from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'due_date', 'created_at', 'is_overdue_display')
    list_filter = ('status', 'priority', 'due_date', 'user')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'
    list_editable = ('status', 'priority')
    readonly_fields = ('created_at', 'user')
    ordering = ('-created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'user')
        }),
        ('Статус и приоритет', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('Метаданные', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return '⚠️ Просрочена'
        return '—'
    is_overdue_display.short_description = 'Просрочка'

    actions = ['mark_as_done', 'mark_as_in_progress']

    @admin.action(description='Отметить как выполненные')
    def mark_as_done(self, request, queryset):
        updated = queryset.update(status=Task.Status.DONE)
        self.message_user(request, f'{updated} задач(и) отмечены как выполненные.')

    @admin.action(description='Перевести в работу')
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status=Task.Status.IN_PROGRESS)
        self.message_user(request, f'{updated} задач(и) переведены в работу.')


# Make admin beautiful
admin.site.site_header = 'Менеджер задач — Администрирование'
admin.site.site_title = 'Task Manager Admin'
admin.site.index_title = 'Управление задачами и пользователями'
