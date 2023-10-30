from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    '''
    Пагинатор для модели Habit
    '''
    page_size = 5
    page_size_query_param = 'per_page'


class UserHabitPaginator(HabitPaginator):
    '''
    Пагинатор для привычек пользователя
    '''
