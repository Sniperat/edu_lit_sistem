from .models import Parent


def user_func(json):
    try:
        user = Parent.objects.get(telegram_user_id=json['message']['chat']['id'])
    except:
        user = Parent(telegram_user_id=json['message']['chat']['id'], state=5)
        user.save()
    return user
#
# def test_func(user):
#     try:
#         test = Test.objects.get(user=user)
#     except:
#         test = Test(user=user)
#         test.save()
#     return test