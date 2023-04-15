from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Test(models.Model):
    users = models.ManyToManyField(User, verbose_name='Пользователи', blank=True)
    name = models.CharField(max_length=512, null=False, blank=False, verbose_name='Название теста')
    questions_number = models.IntegerField(verbose_name="Количество вопросов", default=0)
    description = models.TextField(null=True, blank=True, verbose_name='Описание теста')
    expires_at = models.DateField(verbose_name='Срок сдачи', null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name
    
    def is_expired(self):
        today = date.today()
        if today >= self.expires_at:
            return True
        return False


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True, verbose_name="Текст вопроса")
    image = models.ImageField(upload_to='test_images/', null=True, blank=True, verbose_name='Картинка вопроса')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Вопросы теста'

    def __str__(self):
        return f'{self.test.name} {self.text}' 

    def get_right_answer(self):
        if TestQuestionOption.objects.filter(question=self, is_answer=True).exists():
            return TestQuestionOption.objects.filter(question=self, is_answer=True).first()  
        return None 


class TestQuestionOption(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    text = models.CharField(verbose_name='Текст ответа', null=True, blank=True, max_length=512)
    image = models.ImageField(verbose_name='Картинка ответа', upload_to='test_questions/', null=True, blank=True)
    is_answer = models.BooleanField(default=False, verbose_name='Ответ')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return f'{self.question} {self.text}'
    

class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    choosed_options = models.ManyToManyField(TestQuestionOption, blank=True, verbose_name='Выбранные варианты')
    result = models.IntegerField(verbose_name='Результат', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты теста'

    def __str__(self):
        return f'{self.test.name} {self.user.username}'