from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to="materials/course/images", verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание курса')

    def __str__(self):
        return f'{self.title} - {self.description}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ["title_course"]


class Lesson(models.Model):
    title_lesson = models.CharField(max_length=150, verbose_name='Название урока')
    preview = models.ImageField(upload_to="materials/lesson/images", verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание урока')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Курс', related_names='lesson', null=True, blank=True
    )
    link_to_video = models.URLField(verbose_name='Ссылка на видео')

    def __str__(self):
        return f'{self.title_lesson}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['title_lesson']
