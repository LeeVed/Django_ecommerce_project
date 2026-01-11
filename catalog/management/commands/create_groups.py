from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Создает группу 'Модератор продуктов' с правами на удаление и отмену публикации"

    def handle(self, *args, **options):
        needed_permissions = [
            "delete_product",
            "can_unpublish_product",
        ]
        try:

            content_type = ContentType.objects.get(
                app_label="catalog",
                model="product"
            )

            group, created = Group.objects.get_or_create(   # если не находит указанную группу, создает новую
                name="Модератор продуктов"
            )

            if created:
                self.stdout.write("Создана группа 'Модератор продуктов'")
            else:
                self.stdout.write("Группа 'Модератор продуктов' уже существует")
                # Удаляем старые права если они есть
                group.permissions.clear()

            # Находим и назначаем ТОЛЬКО нужные права
            assigned_permissions = []
            for perm_codename in needed_permissions:
                try:
                    perm = Permission.objects.get(
                        content_type=content_type,
                        codename=perm_codename
                    )
                    group.permissions.add(perm)
                    assigned_permissions.append(perm.name)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Разрешение '{perm_codename}' не найдено!"
                            f"Убедитесь что миграции применены."
                        )
                    )
                    return  # Прерываем выполнение если право не найдено

            if assigned_permissions:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Назначены права:\n"
                        f"  • {chr(10) + '   • '.join(assigned_permissions)}"
                    )
                )

            # Финальная проверка
            group_perms = list(group.permissions.values_list('codename', flat=True))
            self.stdout.write(
                self.style.SUCCESS(
                    f"Итог: группа имеет {len(group_perms)} права: {', '.join(group_perms)}"
                )
            )

        except ContentType.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    '   Ошибка: Модель Product не найдена\n'
                    '   Убедитесь, что:\n'
                    '   1. Приложение "catalog" в INSTALLED_APPS\n'
                    '   2. Выполнены все миграции: python manage.py migrate'
                )
            )
