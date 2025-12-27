# Здравствуй и добро пожаловать на мое ТЗ
Хоть и не прошел его

(наполучал багов)

Я подведу итоги здесь

## Что планировалось 

Сделать дневник у студентов

С правами 

- **Администратор**: может управлять ограничениями доступа при добавлении новых возможностей API приложения и все ниже
перечисленное.
- **Директор**: Назначать и удалять учителей на курсы. Может добавлять и удалять студента в(из) учереждение(ия).
Может следить или вмешиваться в составление учебного плана
- **Учитель**: Может принимать и удалять студентов в(из) группу(ы), составлять учебный план и расписание(создавать, 
изменять, удалять), ставить баллы.
- **Студент**: Может записываться на курсы, смотреть расписание, смотреть баллы за дз и тесты и итоги четверти.

## Что я понял и усвоил за время выполения ТЗ

- сохранить рабочий код прежде чем изменять
- Не справился Mock view(а может и не с ними)
- Пожадничал и хотел изучить новые возможности библиотек и потратил время

Да и вообще потерялся от идей и возможностей как сделать код
От базовых Permission DRF и своих. Так же и библиотек Django Guardian, Django Authority и т.д. 
 С системой Group и user_permission. Поставить можно объект на модель, админку, вьюху.


## Ошибки и код 


 вышло что тест работает а вьюха нет

Регистрация в тестах пропускает а в вьюхе ошибка выходит что c ключом что то не то

(Key (username)=() already exist)


    #/serializer
    class StudentRegSerializer(ModelSerializer):
        first_name = serializers.CharField(required=True)
        second_name = serializers.CharField(required=True)
        last_name = serializers.CharField(required=True)
        email = serializers.EmailField(required=True)
        is_student = serializers.BooleanField(default=True)
        password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True,)

        class Meta:
            model = CustomUser
            fields = ('first_name', 'second_name', 'last_name', 'email', 'is_student', 'password','password2')
            extra_kwargs = {'password': {'write_only': True}}

        def save(self):
            user = CustomUser(
                email=self.validated_data['email'],
                first_name=self.validated_data['first_name'],
                second_name=self.validated_data['second_name'],
                last_name=self.validated_data['last_name'],
                is_student=self.validated_data['is_student'],
            )
            password = self.validated_data['password']
            password2 = self.validated_data['password2']
    
            if password != password2:
                raise serializers.ValidationError({'password': 'Passwords do not match'})
            user.set_password(password)
            user.save()
            return user


    #/views
    class StudentRegisterAPIView(ViewSet):
        permission_classes = [IsAnonymous]
        serializer_class = StudentRegSerializer

    def post(self, request):
        serializer = StudentRegSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(StudentRegSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        #/test
        def test_create_user(self):
        data = {
            'email': 'mail@mail.ru',
            'first_name': 'Дмитрий',
            'second_name': 'Салаткин',
            'last_name': 'Викторович',
            'password': '123',
            'password2': '123',
        }
        response = self.client.post('/api/v1/user/register/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



другой кейс, тест не работает но вьюха работает

в тесте ошибка с ответом(response)

(Expected a `Response`, `HttpResponse` or `StreamingHttpResponse` to be returned from the view, but received a `<class 'dict'>`)

логин происходит и дает refresh и access токены

    #/token
    from rest_framework_simplejwt.tokens import RefreshToken

    def get_token(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


    #/serializer
    class StudentLogSerializer(ModelSerializer):
        email = serializers.EmailField(required=True)

        class Meta:
            model = CustomUser
            fields = ('email', 'password')
            extra_kwargs = {'password': {'write_only': True}}


    /views
    class StudentLoginAPIView(ViewSet):
        permission_classes = [IsAnonymous]
        serializer_class = StudentLogSerializer

        def post(self, request):
    
            serializer = StudentLogSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                    user = authenticate(email=serializer.validated_data['email'],
                                        password=serializer.validated_data['password'])
                except CustomUser.DoesNotExist:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                if user:
                    token = get_token(user)
                    return Response({'message': 'Login successfull',
                                          'token': token}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


    /tests
    @patch('user.views.StudentLoginAPIView.post')
        def test_login(self, mock_user):
            mock_user.return_value = {
                'email': 'mail@mail.ru',
                'first_name': 'Дмитрий',
                'second_name': 'Салаткин',
                'last_name': 'Викторович',
                'password': '123',
                'password2': '123',
            }
            data = {
                'email': 'mail@mail.ru',
                'password': '123',
            }
            client = APIClient()
            response = self.client.post(reverse('login'), data, format='json')
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

## Эмоции и Мнение о ТЗ

Тестовое задание очень интересное, показало мои возможности и 
показало куда мне расти дальше.

Хотелось многое попробовть но не вышло. Вышел пшик пшика. 
Только потратил время на сбор информации и уроки, багфиксы.

Я по итогу дальше буду изучать эту тему все равно, ибо вышло как то не очень.
