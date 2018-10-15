from django.contrib.gis.db import models


class AbstractLocationModel(models.Model):
    country = models.CharField(
        verbose_name='País',
        max_length=100,
        default=''
    )
    state = models.CharField(
        verbose_name='Provincia',
        max_length=100,
        default=''
    )
    city = models.CharField(
        verbose_name='Población',
        max_length=100,
        default=''
    )
    address = models.CharField(
        verbose_name='Dirección',
        max_length=200,
        default=''
    )
    zipcode = models.CharField(
        verbose_name='Código postal',
        max_length=100,
        default=''
    )
    location_string = models.CharField(
        verbose_name='Location string',
        db_index=True,
        max_length=255,
        default='',
        blank=True
    )
    latitude = models.FloatField(
        verbose_name='Latitud',
        blank=True,
        default=0
    )
    longitude = models.FloatField(
        verbose_name='Longitud',
        blank=True,
        default=0
    )
    radius = models.IntegerField(
        verbose_name='Radius',
        blank=True,
        null=True
    )
    point = models.PointField(
        verbose_name='Point',
        srid=4326,
        blank=True,
        null=True
    )
    polygon = models.PolygonField(
        verbose_name='Polígono',
        srid=4326,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Si se ha puesto un radio, pasarlo a int.

        location_string es la concatenación de la dirección completa,
        por lo que solo se crea si existe country, state, city, address y zipcode.
        En caso contrario, sera un string vació (valor default del campo location_string).
        """
        if self.country and self.state and self.city and self.address and self.zipcode:
            self.location_string = '{}, {}, {}, {}, {}'.format(
                self.country,
                self.state,
                self.city,
                self.address,
                self.zipcode
            )
        if self.radius:
            self.radius = int(self.radius)
        super().save(*args, **kwargs)
