import os
from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category
from catalog.models import Product


class Command(BaseCommand):
    help = "Загружает тестовые данные из фикстур"

    def add_arguments(self, parser: object) -> None:
        # Добавляем опциональный аргумент для пути к фикстурам
        parser.add_argument("--fixtures-dir", type=str, default="catalog/fixtures", help="Путь к папке с фикстурами")

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Очистка базы данных...")

        # Удаляем все продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("База данных очищена"))

        # Загружаем фикстуры
        fixtures_dir = options["fixtures_dir"]

        # Проверяем существование файлов
        categories_file = os.path.join(fixtures_dir, "categories.json")
        products_file = os.path.join(fixtures_dir, "products.json")

        if os.path.exists(categories_file):
            self.stdout.write(f"Загрузка фикстур из {categories_file}...")
            try:
                call_command("loaddata", categories_file)
                self.stdout.write(self.style.SUCCESS("Категории загружены"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
        else:
            self.stdout.write(self.style.WARNING(f"Файл {categories_file} не найден. Создаю тестовые категории..."))
            # Создаем тестовые категории если файла нет
            Category.objects.create(name="Тестовая категория 1", description="")
            Category.objects.create(name="Тестовая категория 2", description="")

        if os.path.exists(products_file):
            self.stdout.write(f"Загрузка фикстур из {products_file}...")
            try:
                call_command("loaddata", products_file)
                self.stdout.write(self.style.SUCCESS("Продукты загружены"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
        else:
            self.stdout.write(self.style.WARNING(f"Файл {products_file} не найден. Создаю тестовые продукты..."))
            # Создаем тестовые продукты если файла нет
            category = Category.objects.first()
            if category:
                Product.objects.create(
                    name="Тестовый продукт",
                    description="Описание тестового продукта",
                    category=category,
                    price=1000.00,
                )

        # Выводим итоги
        total_categories = Category.objects.count()
        total_products = Product.objects.count()

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"ИТОГО: {total_categories} категорий, {total_products} продуктов"))
