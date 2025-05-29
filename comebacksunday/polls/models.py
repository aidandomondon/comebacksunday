from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date Published")
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # Note: Entries whose composite key is already present in the
    # db will overwrite the pre-existing entry with the same composite key
    # when .save() is used, since .save() dynamically chooses between INSERTing and UPDATEing.
    # Explicitly use Choice.objects.create() to avoid overwriting.
    pk = models.CompositePrimaryKey("question_id", "choice_text")
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text