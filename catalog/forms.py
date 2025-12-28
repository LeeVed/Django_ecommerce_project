from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продуктов с валидацией"""

    FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    # ВРЕМЕННОЕ ПОЛЕ для демонстрации стилизации чекбокса
    example_checkbox = forms.BooleanField(
        required=False,
        initial=True,
        label="Пример чекбокса для демонстрации",
        help_text="Это поле добавлено для демонстрации стилизации.",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "title": "Это пример правильно стилизованного чекбокса Bootstrap"}
        ),
    )

    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "image"]

    def __init__(self, *args, **kwargs):
        """Настройка стилей и атрибутов для полей формы"""
        super().__init__(*args, **kwargs)
        self._setup_form_fields()

    def _setup_form_fields(self):
        """Основная настройка полей формы"""
        field_configs = {
            "name": {
                "placeholder": "Введите название товара *",
                "title": "Название должно быть уникальным и содержать минимум 3 символа",
                "minlength": "3",
                "maxlength": "200",
            },
            "description": {
                "placeholder": "Опишите ваш продукт...",
                "rows": "4",
                "title": "Подробное описание поможет покупателям лучше понять продукт",
            },
            "price": {
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0.01",
                "title": "Введите цену в рублях",
                "inputmode": "decimal",
            },
            "category": {"title": "Выберите подходящую категорию"},
            "image": {"accept": "image/*", "title": "Загрузите изображение продукта (JPG, PNG, GIF)"},
        }

        # Поля, которые должны быть крупнее
        large_fields = {"description", "image", "price"}

        # Настройка каждого поля
        for field_name, field in self.fields.items():
            field.label = ""

            # Базовый CSS-класс
            self._add_css_class(field, "form-control")

            # Добавляем настройки из словаря
            if field_name in field_configs:
                field.widget.attrs.update(field_configs[field_name])

            # Делаем важные поля крупнее
            if field_name in large_fields:
                self._add_css_class(field, "form-control-lg")

        # Особые настройки для поля category
        if "category" in self.fields:
            self.fields["category"].widget.empty_label = "--- Выберите категорию ---"

    def _add_css_class(self, field, css_class):
        """Безопасно добавляет CSS-класс к полю"""
        current = field.widget.attrs.get("class", "")
        classes = current.split()
        if css_class not in classes:
            classes.append(css_class)
        field.widget.attrs["class"] = " ".join(classes).strip()

    def _get_forbidden_words_in_text(self, text):
        """Общий метод для поиска запрещенных слов в тексте"""
        if not text:
            return []
        text_lower = text.lower()
        return [word for word in self.FORBIDDEN_WORDS if word in text_lower]

    def clean_name(self):
        """Валидация названия на запрещенные слова"""
        name = self.cleaned_data.get("name")
        # Проверка минимальной длины
        if name and len(name.strip()) < 3:
            raise ValidationError("Название должно содержать минимум 3 символа")
        # Проверка запрещенных слов
        found_words = self._get_forbidden_words_in_text(name)
        if found_words:
            raise ValidationError(
                f"Название содержит запрещенные слова: "
                f'{", ".join(found_words[:3])}'  # Показываем первые 3
            )
        return name

    def clean_description(self):
        """Валидация описания на запрещенные слова"""
        description = self.cleaned_data.get("description")
        found_words = self._get_forbidden_words_in_text(description)
        if found_words:
            raise ValidationError(
                f"Описание содержит запрещенные слова: "
                f'{", ".join(found_words[:2])}'  # Показываем первые 2
            )
        return description

    def clean_price(self):
        """Валидация цены"""
        price = self.cleaned_data.get("price")
        if price and price <= 0:
            raise ValidationError("Цена должна быть положительной")
        return price
