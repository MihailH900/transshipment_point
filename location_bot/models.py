from django.db import models

class VK_sender(models.Model):
        user_id = models.TextField(max_length = 100, blank = True)
        meet_location_x = models.TextField(blank = True)
        meet_location_y = models.TextField(blank = True)
        message = models.TextField(blank = True)
        count = models.IntegerField()
