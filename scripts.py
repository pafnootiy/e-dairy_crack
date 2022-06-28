import random

from datacenter.models import Commendation
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Schoolkid

COMMENDATION_SAMPLES = ["Молодец!", " Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!", "Ты меня приятно удивил!",
                        "Великолепно!", "Прекрасно!", "Ты меня очень обрадовал!",
                        "Именно этого я давно ждал от тебя!", "Сказано здорово – просто и ясно!",
                        "Ты, как всегда, точен!", "Очень хороший ответ!", "Талантливо!",
                        "Ты сегодня прыгнул выше головы!", "Я поражен!", "Потрясающе!",
                        "Замечательно!", "Прекрасное начало!", "Так держать!", "Ты на верном пути!", "Здорово!",
                        "Это как раз то, что нужно!", "Я тобой горжусь!", "С каждым разом у тебя получается всё лучше!",
                        "Мы с тобой не зря поработали!", "Я вижу, как ты стараешься!", "Ты растешь над собой!",
                        "Ты многое сделал, я это вижу!",
                        "Теперь у тебя точно все получится!"]


def remove_chastisements(child_account):
    chastisements = Chastisement.objects.filter(schoolkid=child_account)
    chastisements.delete()
    return chastisements


def fix_marks(child_account):
    bad_marks_update = Mark.objects.filter(schoolkid=child_account, points__lte=3).update(points=5)
    return bad_marks_update


def create_commendation(child_name, child_account, lesson_name, COMMENDATION_SAMPLES):
    default_name = "Фролов Иван"

    if child_name == default_name:
        commendation = random.choice(COMMENDATION_SAMPLES)
        try:
            lesson = Lesson.objects.filter(group_letter="А", year_of_study=6,
                                           subject__title__contains=lesson_name).first()

            public_commendation = Commendation.objects.create(text=commendation, schoolkid=child_account,
                                                              subject=lesson.subject,
                                                              teacher=lesson.teacher, created=lesson.date)
        except AttributeError:
            print("Неверное введено название предмета")
        else:
            return public_commendation


def main():
    child_name = input("Введите имя ученика: ")
    lesson_title = input("Введите название урока: ")

    try:
        child_account = Schoolkid.objects.get(full_name__contains=f"{child_name}")

    except Schoolkid.MultipleObjectsReturned:
        print("Найденно больше чем 1 совпадение , введите корректные данные")
    except Schoolkid.DoesNotExist:
        print("Такого ученика не существует ,введите корректные данные")
    except:
        print("Введите корректное имя ученика и/или название предмета")
    else:
        remove_chastisements(child_account)
        fix_marks(child_account)
        create_commendation(child_name, child_account, lesson_title, COMMENDATION_SAMPLES)


if __name__ == "__main__":
    main()
