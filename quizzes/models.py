from django.db import models
from teachers.models import TeacherProfile
from classes.models import Class
from students.models import StudentProfile
# Create your models here.

class Quiz(models.Model):
    created_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)
    created_for = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    questions = models.ManyToManyField('quizzes.Question')
    posted = False

    class Meta:
        verbose_name_plural = "quizzes"

    def post(self):
        self.posted = True
    
    def __str__(self) -> str:
        return f"Quiz({self.name} for {self.created_for.name})"

class Question(models.Model):
    created_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)
    body = models.TextField(max_length=1000)
    correct_answer = models.ForeignKey('quizzes.AnswerChoice')
    incorrect_answers = models.ManyToManyField('quizzes.AnswerChoice')

    def __str__(self) -> str:
        return f"Q({self.body[:20]})"

class QuizSolution(models.Models):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    submitted = False

    class Meta:
        verbose_name = "Quiz Solution"
        verbose_name_plural = "Quiz Solutions"
        unique_together = ('quiz', 'student')
    
    def submit(self):
        self.submitted = True

    def __str__(self) -> str:
        return (self.student, self.quiz)

class AnswerChoice(models.Model):
    created_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)
    body = models.TextField(max_length=1000)

    def __str__(self) -> str:
        return self.body

class Answer(models.Model):
    quiz_solution = models.ForeignKey(QuizSolution, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)

    def correct(self):
        if self.body == self.question.correct_answer:
            return True
        return False

class Score(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_solution = models.OneToOneField(QuizSolution, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(max_length=5, null=True, blank=True)
    total_questions = models.IntegerField(max_length=5, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.quiz_solution}: {self.correct_answers / self.total_questions}"




