from django import forms
from django.contrib.auth.models import User
from app.models import Profile, Question, Tag, Answer
from django.contrib.auth import hashers

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=False,
        widget=forms.TextInput(
            attrs={'required': True}
        )
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        required=False,
        widget=forms.PasswordInput(
            attrs={'required': True}
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("No user with this username")
        if len(username) < 2:
            raise forms.ValidationError("Username is too short")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError("Password length must be > 8")
        return password


class RegisterForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.TextInput(
            attrs={'required': True}
        )
    )
    username = forms.CharField(
        required=False,
        label="Username",
        max_length=150, # TODO
        widget=forms.TextInput(
            attrs={'required': True}
        )
    )
    password = forms.CharField(
        required=False,
        label="Password",
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={'required': True}
        )
    )
    repeated = forms.CharField(
        required=False,
        label="Repeat password",
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={'required': True}
        )
    )
    avatar = forms.ImageField(
        required=False,
        label="Upload avatar",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "type": "file",
                "id": "formFile",
                "enctype": "multipart/form-data",
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Account with such email already exists")

        if len(email) < 5:
            print("email")
            raise forms.ValidationError("Email length must be at least 5 symbols")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        
        if len(username) < 4:
            print("username")
            raise forms.ValidationError("Username length must be > 4")
        return username
        
    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            print("password")
            raise forms.ValidationError("Password length must be > 8")
        return password

    def clean_repeated_password(self):
        password = self.cleaned_data['password']
        repeated_password = self.cleaned_data['repeated']
        
        if password != repeated_password:
            print("passwor match")
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data
    
    def save(self):
        super().clean()

        try:
            self.cleaned_data.pop("repeated")
        except Exception as ex:
            pass

        avatar = self.cleaned_data.pop("avatar", None)
        
        new_user = User.objects.create_user(**self.cleaned_data)
        profile = Profile.objects.create(user=new_user, avatar=avatar)

        return new_user


class SettingsForm(forms.Form):
    email = forms.CharField(
        label="Email",
        required=False,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'type': 'email',
            },
        ),
    )
    username = forms.CharField(
        label="Username",
        required=False,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'min-length': 3,
            }
        )
    )
    avatar = forms.ImageField(
        label="Upload avatar",
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    # class Meta:
    #     model = User
    #     fields = ["email", "username"]

    def clean_email(self):
        email = self.cleaned_data['email']

        if len(email) < 5:
            raise forms.ValidationError("Email length must be more than 4")
        if '@' not in email:
            raise forms.ValidationError("Invalid email!")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 3:
            raise forms.ValidationError("Username length must be more than 2")
        if User.objects.filter(email=username).exists():
            raise forms.ValidationError("Such username is already in use")
        return username

    def clean_avatar(self):
        avatar = self.files.get('avatar', None)
        if avatar and avatar.size > 5 * 1024 * 1024: 
            raise forms.ValidationError("The avatar size must be less than 5MB!")
        return avatar

    def save(self, user_id):
        users_with_such_email = User.objects.filter(email=self.cleaned_data.get("email", ""))
        if users_with_such_email.count() == 0 or (users_with_such_email.count() == 1 and users_with_such_email[0].id == user_id):
            User.objects.filter(id=user_id).update(
                email=self.cleaned_data.get("email", ""),
            )
        else:
            self.add_error("email", "Such email is already being used")

        users_with_such_username = User.objects.filter(username=self.cleaned_data.get("username", ""))
        if users_with_such_username.count() == 0 or (users_with_such_username.count() == 1 and users_with_such_username[0].id == user_id):
            User.objects.filter(id=user_id).update(
                username=self.cleaned_data.get("username", ""),
            )
        else:
            self.add_error("username", "Such username is already being used")

        avatar = self.files.get("avatar", None)
        if avatar:
            profile = Profile.objects.get(user_id=user_id)
            profile.avatar = avatar
            profile.save()


class AskForm(forms.Form):
    title = forms.CharField(
        label="Title",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'title-input',
                'placeholder': 'In a nutshell',
                'required': True,
                'min-length': 11,
                'max-length': 100,
            },
        ),
    )
    description = forms.CharField(
        label="Text",
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'text-input textarea-input',
                'type': 'text',
                'placeholder': 'Describe in details',
                'max-length': 1000,
            }
        )
    )
    tags = forms.CharField(
        label="Tags",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'tags-input',
                'placeholder': 'List tags by comma',
                'max-length': 100,
            }
        )
    )

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) < 10:
            raise forms.ValidationError("Title length must be more than 10")
        if len(title) >= 100:
            raise forms.ValidationError("Title length must be less than 100")
        try:
            Question.objects.get(title=title)
            raise forms.ValidationError("Such question already exists")
        except Question.DoesNotExist:
            pass
        return title


    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 0:
            try:
                Question.objects.get(description=description)
                raise forms.ValidationError("Such question already exists")
            except Question.DoesNotExist:
                pass
        return description


    def clean_tags(self):
        tags = self.cleaned_data['tags']

        tag_list = list()
        if len(tags) != 0:
            raw_tags = tags.split(',')
            for tag in raw_tags:
                tag_list.append(tag.strip(" "))

            for i, tag in enumerate(tag_list):
                if tag in tag_list[:i] + tag_list[i + 1:]:
                    raise forms.ValidationError(f"Tags '{tag}' is not unique")
                if len(tag) > 32:
                    raise forms.ValidationError("Tag len must be lower than 33")
                
                for c in tag:
                    if not c.isalpha():
                        raise forms.ValidationError("Tags should contain only alpha symbols")
        return tags

    def save(self, user) -> int:
        new_question = Question.objects.create(
            author=Profile.objects.filter(user=user)[0],
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
        )
        for tag in self.cleaned_data.get('tags', '').split(","):
            try:
                existing_tag = Tag.objects.get(word=tag.strip(" "))
                new_question.tags.add(existing_tag)
            except Tag.DoesNotExist:
                new_tag = Tag.objects.create(word=tag.strip(" "))
                new_question.tags.add(new_tag)
        return new_question.id


class AnswerForm(forms.Form):
    answer = forms.CharField(
        required=False,
        min_length=4,
        max_length=490,
        widget=forms.Textarea(
            attrs={
                "class": "textarea-input answer-input",
                "required": "True",
                "placeholder": "Enter your answer here...",
                "autocomplete": "off",
                "type": "text",
            }
        )
    )

    def clean_answer(self):
        answer = self.cleaned_data["answer"]
        if len(answer) < 4 or len(answer) > 490:
            raise forms.ValidationError("Wrong length of the answer")
        return answer

    def save(self, user, question) -> int:
        new_answer = Answer.objects.create(
            question=question,
            description=self.cleaned_data.get("answer", ""),
            author=Profile.objects.filter(user=user)[0],
        )
        return new_answer.id