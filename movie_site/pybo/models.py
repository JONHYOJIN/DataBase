# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actor(models.Model):
    actor_code = models.IntegerField(primary_key=True)
    actor_name = models.CharField(max_length=100, blank=True, null=True)
    original_actor_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actor'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Director(models.Model):
    director_code = models.IntegerField(primary_key=True)
    director_name = models.CharField(max_length=100, blank=True, null=True)
    original_director_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'director'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Image(models.Model):
    movie_code = models.OneToOneField('Movie', models.DO_NOTHING, db_column='movie_code', primary_key=True)
    image_url = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'image'
        unique_together = (('movie_code', 'image_url'),)


class Jenre(models.Model):
    movie_code = models.OneToOneField('Movie', models.DO_NOTHING, db_column='movie_code', primary_key=True)
    jenre_name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'jenre'
        unique_together = (('movie_code', 'jenre_name'),)


class Movie(models.Model):
    movie_code = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    original_title = models.CharField(max_length=100, blank=True, null=True)
    opening_date = models.DateTimeField(blank=True, null=True)
    playing_time = models.IntegerField(blank=True, null=True)
    domestic_rate = models.CharField(max_length=10, blank=True, null=True)
    foreign_rate = models.CharField(max_length=10, blank=True, null=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    content = models.CharField(max_length=2000, blank=True, null=True)
    poster_url = models.CharField(max_length=512, blank=True, null=True)
    audience_rate = models.FloatField(blank=True, null=True)
    journalist_rate = models.FloatField(blank=True, null=True)
    netizen_rate = models.FloatField(blank=True, null=True)
    audience_count = models.IntegerField(blank=True, null=True)
    journalist_count = models.IntegerField(blank=True, null=True)
    netizen_count = models.IntegerField(blank=True, null=True)
    cumulative_audience = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie'


class MovieActor(models.Model):
    movie_code = models.OneToOneField(Movie, models.DO_NOTHING, db_column='movie_code', primary_key=True)
    actor_code = models.ForeignKey(Actor, models.DO_NOTHING, db_column='actor_code')
    cast = models.CharField(max_length=5, blank=True, null=True)
    role = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_actor'
        unique_together = (('movie_code', 'actor_code'),)


class MovieDirector(models.Model):
    movie_code = models.OneToOneField(Movie, models.DO_NOTHING, db_column='movie_code', primary_key=True)
    director_code = models.ForeignKey(Director, models.DO_NOTHING, db_column='director_code')

    class Meta:
        managed = False
        db_table = 'movie_director'
        unique_together = (('movie_code', 'director_code'),)


class MovieReview(models.Model):
    movie_code = models.OneToOneField(Movie, models.DO_NOTHING, db_column='movie_code', primary_key=True)
    review_code = models.ForeignKey('Review', models.DO_NOTHING, db_column='review_code')

    class Meta:
        managed = False
        db_table = 'movie_review'
        unique_together = (('movie_code', 'review_code'),)


class Nation(models.Model):
    movie_code = models.OneToOneField(Movie, models.DO_NOTHING, db_column='movie_code', primary_key=True)
    country = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'nation'
        unique_together = (('movie_code', 'country'),)


class Point(models.Model):
    movie_code = models.OneToOneField(Movie, models.DO_NOTHING, db_column='movie_code', primary_key=True)
    point_id = models.CharField(max_length=30)
    point_content = models.CharField(max_length=500, blank=True, null=True)
    point_date = models.DateTimeField(blank=True, null=True)
    point_good = models.IntegerField(blank=True, null=True)
    point_bad = models.IntegerField(blank=True, null=True)
    point_star = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'point'
        unique_together = (('movie_code', 'point_id'),)


class Review(models.Model):
    review_code = models.IntegerField(primary_key=True)
    review_id = models.CharField(max_length=30, blank=True, null=True)
    review_title = models.CharField(max_length=100, blank=True, null=True)
    review_content = models.CharField(max_length=2000, blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)
    review_lookup = models.IntegerField(blank=True, null=True)
    review_recommend = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'


class Review2(models.Model):
    review_code = models.OneToOneField(Review, models.DO_NOTHING, db_column='review_code', primary_key=True)
    review2_id = models.CharField(max_length=30)
    review2_content = models.CharField(max_length=500, blank=True, null=True)
    review2_date = models.DateTimeField(blank=True, null=True)
    review2_good = models.IntegerField(blank=True, null=True)
    review2_bad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review2'
        unique_together = (('review_code', 'review2_id'),)


class Video(models.Model):
    movie_code = models.OneToOneField(Movie, models.DO_NOTHING, db_column='movie_code', primary_key=True)
    video_url = models.CharField(max_length=512)
    video_title = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video'
        unique_together = (('movie_code', 'video_url'),)
