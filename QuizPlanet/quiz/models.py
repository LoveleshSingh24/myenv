from django.db import models
import pandas as pd
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 15)
    class Meta:
        verbose_name_plural= 'Categories'
    def __str__(self):
        return self.name

class Quiz(models.Model):
    title=models.CharField(max_length=255)
    description= models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    quiz_file = models.FileField(upload_to='quiz/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural= "Quizzes"
    
    def  __str__(self):
        return self.title
    
    # call the function on quize save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.quiz_file:
            if self.quiz_file.name.endswith('.xlsx'):
                self.import_quiz_from_excel()
            elif self.quiz_file.name.endswith('.csv'):
                self.import_quiz_from_csv()

    #fumction to extract exel file
    def import_quiz_from_excel(self):
        # Read the CSV file using pandas
        df = pd.read_excel(self.quiz_file.path)
        # Clean up column names by stripping leading and trailing spaces
        df.columns = df.columns.str.strip()
        print(df.columns)
        # Iterate over each row
        for index, row in df.iterrows():
            # Extract question text, choices, and correct answer from the row
            question_text = row['Question']
            choice1 = row['A']
            choice2 = row['B']
            choice3 = row['C']
            choice4 = row['D']
            correct_answer = row['Answer']

            # Create the question object 
            question = Question.objects.get_or_create(quiz=self, text=question_text)
            
            # Create choices objects[0]
            choice_1 = Choice.objects.get_or_create(question=question[0], text=choice1, is_correct=(correct_answer == 'A'))
            choice_2 = Choice.objects.get_or_create(question=question[0], text=choice2, is_correct=(correct_answer == 'B'))
            choice_3 = Choice.objects.get_or_create(question=question[0], text=choice3, is_correct=(correct_answer == 'C'))
            choice_4 = Choice.objects.get_or_create(question=question[0], text=choice4, is_correct=(correct_answer == 'D'))
    

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    text=models.TextField()

    def  __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    text= models.CharField(max_length=255)
    is_correct  = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:50]},{self.text[:20]}"
    
class QuizSubmission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.quiz.title}"

class UserRank(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    rank=models.IntegerField(null=True,blank =True)
    total_score = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.rank}, {self.user.username}"

@receiver(post_save, sender=QuizSubmission)
def updated_leaderboard(sender, instance, created, **kwargs):
    if created:
        update_leaderboard()


def update_leaderboard():
    # Count the sum of all users' scores
    user_scores = QuizSubmission.objects.values('user').annotate(total_score=Sum('score')).order_by('-total_score')

    # Update rank based on the sorted list
    rank = 1
    for entry in user_scores:
        user_id = entry['user']
        total_score = entry['total_score']

        # Retrieve User instance
        user = User.objects.get(id=user_id)
        
        # Check if UserRank already exists for this user
        user_rank, created = UserRank.objects.get_or_create(user=user)
        
        # Update UserRank fields
        user_rank.rank = rank
        user_rank.total_score = total_score
        user_rank.save()

        rank += 1
