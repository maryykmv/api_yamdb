import csv
from collections import namedtuple

from django.conf import settings
from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

model_tuple = namedtuple('Model', ['base', 'model', 'fields'])

user = model_tuple('users.csv', User, [
    'id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name'])
category = model_tuple('category.csv', Category, [
    'id', 'name', 'slug'])
genre = model_tuple('genre.csv', Genre, [
    'id', 'name', 'slug'])
title = model_tuple('titles.csv', Title, [
    'id', 'name', 'year', 'category_id'])
review = model_tuple('review.csv', Review, [
    'id', 'title_id', 'text', 'author_id', 'score', 'pub_date'])
comment = model_tuple('comments.csv', Comment, [
    'id', 'review_id', 'text', 'author_id', 'pub_date'])
genre_title = model_tuple('genre_title.csv', GenreTitle, [
    'id', 'title_id', 'genre_id'])

models = (user, category, genre, title, genre_title, review, comment, )


class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **kwargs):
        for model in models:
            try:
                with open(
                    f'{settings.BASE_DIR}/static/data/{model.base}',
                    'r', encoding='utf-8'
                ) as csv_file:
                    reader = csv.DictReader(csv_file)
                    if reader.fieldnames != model.fields:
                        raise BaseException(
                            f'Проверьте поля в файле {model.base}'
                            f', требуемые поля: {model.fields}')
                    model.model.objects.bulk_create(
                        model.model(**data) for data in reader)
            except IntegrityError:
                pass
            except FileNotFoundError:
                raise BaseException(
                    f'Ошибка при импорте файла базы данных. '
                    f'Проверьте наличие файла {model.base} '
                    f'по адресу: {settings.BASE_DIR}/static/data/')
        self.stdout.write(self.style.SUCCESS('Successfully load data'))
