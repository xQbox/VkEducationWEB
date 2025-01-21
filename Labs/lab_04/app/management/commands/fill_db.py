from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from app.models import Question, Answer, Profile, Tag, QuestionReaction, AnswerReaction
from faker import Faker
from random import randint, choice
from django.utils import timezone
import datetime
from random import sample

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['num']

        if ratio != None:
            try:
                ratio = int(ratio)
            except TypeError:
                return
        else:
            ratio = 10

        users_amount = ratio
        questions_amount = ratio * 10
        answers_amount = ratio * 100
        tags_amount = ratio
        actions_amount = ratio * 200

        # USERS

        users = []

        for _ in range(users_amount):
            users.append(
                User(
                    email=fake.email(),
                    username=fake.user_name() + fake.user_name()[::-1],
                    password=str(fake.password()),
                    date_joined=timezone.now() + datetime.timedelta(seconds=randint(0, 31536000))
                )
            )

        User.objects.bulk_create(users)

        # PROFILES

        print("Creating Profiles...")

        profiles = []
        for i in range(users_amount):
            profiles.append(
                Profile(
                    user=users[i],
                    rating=str(randint(0, 135))
                )
            )

        Profile.objects.bulk_create(profiles)

        print("Profiles Created!")

        # TAGS

        print("Creating Tags...")

        tags = []

        for _ in range(tags_amount):
            tag_word = fake.word() + fake.word()

            tags.append(
                Tag(
                    word=''.join(sample(tag_word, len(tag_word)))
                )
            )

        Tag.objects.bulk_create(tags)

        print("Tags Created!")

        # QUESTIONS

        print("Creating Question...")

        questions = []

        for i in range(questions_amount):
            print('\rCompleted: {}%'.format(round(i * 100 / questions_amount, 1)), end='')

            questions.append(
                Question(
                    title=fake.sentence(8),
                    description=fake.sentence(randint(30, 100)),
                    author=profiles[randint(0, users_amount - 1)],
                    creation_date=timezone.now() + datetime.timedelta(seconds=randint(0, 31536000))
                )
            )

        Question.objects.bulk_create(questions)

        print("\rQuestions created!")

        # TAGS FOR QUESTIONS

        print("Linking tags...")

        for i in range(questions_amount):
            print('\rCompleted: {}%'.format(round(i * 100 / questions_amount, 1)), end='')

            for _ in range(randint(1, 4)):
                if tags_amount > 1:
                    questions[i].tags.add(tags[randint(1, tags_amount - 1)])
                else:
                    print("Недостаточно тегов для присвоения.")

        print("\rTags linked to questions!")

        # REACTIONS FOR QUESTIONS

        print("Creating Question Likes...")

        q_reactions = []

        for i in range(questions_amount):
            if i % 10:
                print('\rCompleted: {}%'.format(round(i * 100 / questions_amount, 1)), end='')

            for _ in range(randint(3, 10)):
                q_reactions.append(
                    QuestionReaction(
                        question=questions[i],
                        profile=profiles[randint(0, users_amount - 1)],
                        reaction_type=choice(["L", "L", "D"])
                    )
                )

        QuestionReaction.objects.bulk_create(q_reactions)

        print("\rQuestion Likes created!")

        # ANSWERS

        print("Creating Answers...")

        answers = []

        for i in range(answers_amount):
            if i % 100:
                print('\rCompleted: {}%'.format(round(i * 100 / answers_amount, 1)), end='')

            answers.append(
                Answer(
                    question=questions[randint(0, questions_amount - 1)],
                    description=fake.sentence(randint(20, 50)),
                    author=profiles[randint(0, users_amount - 1)],
                    is_correct=randint(0, 1),
                    creation_date=timezone.now() + datetime.timedelta(seconds=randint(0, 31536000))
                )
            )

        Answer.objects.bulk_create(answers)

        print("\rAnswers created!  ")

        # REACTIONS FOR ANSWERS

        model_type = ContentType.objects.get_for_model(answers[0])

        a_reactions = []

        print("Creating Answer likes...")

        for i in range(answers_amount):
            if i % 100 == 0:
                print('\rCompleted: {}%'.format(round(i * 100 / answers_amount, 1)), end='')

            for _ in range(randint(1, 4)):
                a_reactions.append(
                    AnswerReaction(
                        answer=answers[i],
                        profile=profiles[randint(0, users_amount - 1)],
                        reaction_type=choice(["L", "L", "L", "D", "D"])
                    )
                )

        AnswerReaction.objects.bulk_create(a_reactions)

        print("\rAnswer likes created!")