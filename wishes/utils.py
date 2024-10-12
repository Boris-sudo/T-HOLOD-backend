from .models import Wishes


def check_wishes(pk):
    wishes = Wishes.objects.filter(id=pk)

    if not wishes.exists():
        return None
    
    return wishes.first()
