import pytest
import aiohttp

from http import HTTPStatus


class TestApi:

    @pytest.mark.parametrize('last_name, first_name, faculty, course, mark', [
        ('Иванов', 'Алексей', 'ФКН', 'ИКТ', 4),  # стандартный случай
        ('А', 'Б', 'X', 'Y', 0),  # граничные короткие строки и минимальная оценка
        ('Петров', 'Максим', 'ФИЗФАК', 'ФТФ', 5),  # максимальная оценка
        ('李', '王', '工学院', '计算机', 3),  # юникод/иностранные символы
        ('ФамилияСОченьДлиннымИмeнeм', 'ИмяСОченьДлиннымИмeнeм',
         'ОченьДлинныйФакультет', 'ОченьДлинныйКурс', 2),  # длинные строки
        ("O'Connor", "Jean-Luc", 'ФМХФ', 'ФТФ-1', 5),  # специальные символы
    ])
    @pytest.mark.asyncio(loop_scope='session')
    async def test_add_stud(self, last_name, first_name, faculty, course, mark, base_url_api):
        async with aiohttp.ClientSession() as session:
            req_url = f'{base_url_api}/add_stud/'

            query_data = {
                'last_name': last_name,
                'first_name': first_name,
                'faculty': faculty,
                'course': course,
                'mark': mark
            }

            response = await session.post(req_url, json=query_data)
            assert response.status == HTTPStatus.ACCEPTED

            # Проверка, что студент появился в таблице
            get_url = f'{base_url_api}/get_students/'
            response_get = await session.get(get_url)
            assert response_get.status == HTTPStatus.OK

            students = await response_get.json()
            assert any(
                s['last_name'] == last_name and s['first_name'] == first_name and s['faculty'] == faculty
                and s['course'] == course and s['mark'] == mark for s in students
            ), "Added student not found in the list"

    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_students(self, base_url_api):
        async with aiohttp.ClientSession() as session:
            get_url = f'{base_url_api}/get_students/'
            response = await session.get(get_url)

            assert response.status == HTTPStatus.OK

            data = await response.json()
            assert isinstance(data, list)
            assert len(data) > 0 or data == []

            sample = data[0]
            expected_keys = {'id', 'last_name', 'first_name', 'faculty', 'course', 'mark'}
            assert expected_keys.issubset(sample.keys())

    @pytest.mark.parametrize('id', [1, 2, 40, 99])
    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_student_by_id(self, id, base_url_api):
        async with aiohttp.ClientSession() as session:
            get_url = f'{base_url_api}/get_student_by_id/?id={id}'
            response = await session.get(get_url)

            status = response.status

            if status == HTTPStatus.OK:
                data = await response.json()
                # Если возвращается объект, а не список:
                expected_keys = {'id', 'last_name', 'first_name', 'faculty', 'course', 'mark'}
                assert expected_keys.issubset(data.keys())
            else:
                error_data = await response.json()
                assert 'detail' in error_data

    @pytest.mark.parametrize('id, last_name, first_name, faculty, course, mark', [
        (1, 'Серега', 'Шуманов', 'ФфКН', 'ИыКТ', 12)
    ])
    @pytest.mark.asyncio(loop_scope='session')
    async def test_update_stud(self, id, last_name, first_name, faculty, course, mark, base_url_api):
        async with aiohttp.ClientSession() as session:
            req_url = f'{base_url_api}/update_stud/?id={id}'

            query_data = {
                'last_name': last_name,
                'first_name': first_name,
                'faculty': faculty,
                'course': course,
                'mark': mark
            }

            response = await session.patch(req_url, json=query_data)
            assert response.status == HTTPStatus.ACCEPTED

            # Проверка, что студент появился в таблице
            get_url = f'{base_url_api}/get_student_by_id/?id={id}'
            response_get = await session.get(get_url)
            assert response_get.status == HTTPStatus.OK

            student = await response_get.json()
            assert student['last_name'] == last_name
            assert student['first_name'] == first_name
            assert student['faculty'] == faculty
            assert student['course'] == course
            assert student['mark'] == mark

    @pytest.mark.parametrize('faculty', ['ФИЗФАК', 'ФМХФ'])
    @pytest.mark.asyncio(loop_scope='session')
    async def test_get_studs_by_fac(self, faculty, base_url_api):
        async with aiohttp.ClientSession() as session:
            req_url = f'{base_url_api}/get_stfac/?faculty={faculty}'
            get_url = f'{base_url_api}/get_students/'

            response_studs = await session.get(get_url)
            data = await response_studs.json()
            assert isinstance(data, list)
            assert len(data) > 0

            response = await session.get(req_url)
            assert response.status == HTTPStatus.OK
            data = await response.json()
            assert isinstance(data, list)
            assert all(student["faculty"] == faculty for student in data)



    @pytest.mark.asyncio(loop_scope='session')
    async def test_clear_studs(self, base_url_api):
        async with aiohttp.ClientSession() as session:
            req_url = f'{base_url_api}/clear_students/'
            get_url = f'{base_url_api}/get_students/'

            # Проверяем, что в базе студенты есть
            response_before = await session.get(get_url)
            data_before = await response_before.json()
            assert isinstance(data_before, list)
            assert len(data_before) > 0, "Ожидается что база будет не пустой перед отчисткой"

            response_clear = await session.get(req_url)
            assert response_clear.status == HTTPStatus.OK

            data_clear = await response_clear.json()
            assert data_clear == {"message": "All students cleared"}

            # Проверяем, что база после очистки пуста
            response_after = await session.get(get_url)
            data_after = await response_after.json()
            assert data_after == {"detail": "Студентов в базе нет"}
