from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import *


class TestQuestionInline(NestedStackedInline):
    model = TestQuestionOption
    extra = 1
    fk_name = 'question'


class TestQuestionInline(NestedStackedInline):
    model = TestQuestion
    extra = 1
    fk_name = 'test'
    inlines = [TestQuestionInline, ]


@admin.register(Test)
class TestAdmin(NestedModelAdmin):
    inlines = [TestQuestionInline,]
    list_display = ('name', 'questions_number', 'expires_at')
    search_fields = ['name', 'users__name']
    filter_horizontal = ('users', )

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test', 'user', 'result')
    readonly_fields = ('choosed_options', 'created_at')