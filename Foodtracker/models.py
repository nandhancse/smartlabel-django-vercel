from django.db import models


class CanteenItems(models.Model):
    """
    Model representing a canteen item/snack with nutritional information.
    """
    item_name = models.TextField(primary_key=True)
    price_rs = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    protein_g = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    calories_kcal = models.IntegerField(blank=True, null=True)
    rating_out_of_5 = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'canteen_items'

    def __str__(self):
        return self.item_name

    def get_rating_stars(self):
        """
        Helper method to get the number of filled stars for display.
        Returns a list of boolean values indicating filled (True) or empty (False) stars.
        """
        if self.rating_out_of_5 is None:
            return [False] * 5

        rating = float(self.rating_out_of_5)
        stars = []
        for i in range(1, 6):
            if i <= rating:
                stars.append(True)
            elif i - 0.5 <= rating:
                stars.append(True)  # Half star
            else:
                stars.append(False)
        return stars


