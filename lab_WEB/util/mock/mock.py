from blog.models import Question, Answer, Profile, Tag
import random

# Mocks
POPULAR_TAGS = [tag for tag in "Cooking,Chicken,Pollos,Fring,Albuquerque,Laundry,Blue,Tight".split(",")]
MEMBERS = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]


# Mock generator
def make_question(amount: int) -> [Question]:
    questions = list()

    for i in range(amount):
        q = Question()
        q.id = 347923 + i
        q.title = "How to cook chicken properly?"
        description = "Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy? Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy? Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy? Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy?"
        q.description = description
        q.author = User()
        q.author.username = random.choice(["Flynn", "Walter Hartwell White Jr.", "Walt Jr."]) 
        q.creation_date = "%02d.%02d.%04d" % (random.randint(1, 28), random.randint(1, 12), random.randint(2007, 2023))

        tags = list()
        for _ in range(2):
            tags.append(Tag(word=random.choice(POPULAR_TAGS)))
        q.tags.set(tags)

        q.rating = round(random.randint(-20, 20))
        questions.append(q)

    return questions


def make_anwers(amount: int) -> [Answer]:
    answers = list()

    for i in range(amount):
        a = Answer()
        a.id = 576 + i

        description_sentances = "First, Gus gets deliveries every day, so the food is always fresh.| Second, Gus is almost always on the premises so the workers are on the ball.| Three, Gus is actually a good boss.| He hires ambitious people to manage, makes sure people work the shifts they want, and is generally helpful.".split('|')
        description = ''.join(description_sentances[:random.randint(1, 5)])
        a.description = description

        a.author = User()
        a.author.username = random.choice(["Sam", "Bob", "Thomas", "Joseph", "Michael", "Charles"]) 
        a.creation_date = "%02d.%02d.%04d" % (random.randint(1, 28), random.randint(1, 12), random.randint(2007, 2023))
        a.is_correct = random.randint(0, 1)
        a.rating = random.randint(-20, 20)
        answers.append(a)

    return answers
