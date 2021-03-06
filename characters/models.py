from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    level = models.IntegerField(default=1)
    ALIGNMENT_CHOICES = (
        ('Unaligned', 'Unaligned'),
        ('LG', 'Lawful Good'),
        ('NG', 'Neutral Good'),
        ('CG', 'Chaotic Good'),
        ('LN', 'Lawful Neutral'),
        ('N', 'Neutral'),
        ('CN', 'Chaotic Neutral'),
        ('LE', 'Lawful Evil'),
        ('NE', 'Neutral Evil'),
        ('CE', 'Chaotic Evil'),
    )
    alignment = models.CharField(
        max_length=255,
        choices=ALIGNMENT_CHOICES,
        default='Neutral',
    )
    SIZE_CHOICES = (
        ('Tiny', 'Tiny'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('Huge', 'Huge'),
        ('Gargantuan', 'Gargantuan'),
    )
    size = models.CharField(
        max_length=255,
        choices=SIZE_CHOICES,
        default='Medium',
    )
    languages = models.CharField(max_length=255, blank=True)
    strength = models.IntegerField(default=10, blank=True)
    dexterity = models.IntegerField(default=10, blank=True)
    constitution = models.IntegerField(default=10, blank=True)
    intelligence = models.IntegerField(default=10, blank=True)
    wisdom = models.IntegerField(default=10, blank=True)
    charisma = models.IntegerField(default=10, blank=True)
    armor_class = models.IntegerField(default=0, blank=True)
    hit_points = models.CharField(max_length=255, blank=True)
    speed = models.CharField(max_length=255, default='', blank=True)
    saving_throws = models.CharField(max_length=255, default='', blank=True)
    skills = models.CharField(max_length=255, default='', blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Monster(Character):
    creature_type = models.CharField(max_length=255, default='', blank=True)
    damage_vulnerabilities = models.CharField(max_length=255, default='', blank=True)
    damage_immunities = models.CharField(max_length=255, default='', blank=True)
    damage_resistances = models.CharField(max_length=255, default='', blank=True)
    condition_immunities = models.CharField(max_length=255, default='', blank=True)
    senses = models.CharField(max_length=255, default='', blank=True)
    challenge_rating = models.CharField(max_length=255, default='', blank=True)
    traits = models.TextField(blank=True)
    actions = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('characters:monster_detail', kwargs={
            'monster_pk': self.pk
            })


class NPC(Character):
    npc_class = models.CharField(verbose_name= _('Class'),max_length=255, default='', blank=True)
    age = models.CharField(max_length=255, default='', blank=True)
    height = models.CharField(max_length=255, default='', blank=True)
    weight = models.CharField(max_length=255, default='', blank=True)
    creature_type = models.CharField(max_length=255, default='', blank=True)
    damage_vulnerabilities = models.CharField(max_length=255, default='', blank=True)
    damage_immunities = models.CharField(max_length=255, default='', blank=True)
    damage_resistances = models.CharField(max_length=255, default='', blank=True)
    condition_immunities = models.CharField(max_length=255, default='', blank=True)
    senses = models.CharField(max_length=255, default='', blank=True)
    challenge_rating = models.CharField(max_length=255, default='', blank=True)
    traits = models.TextField(blank=True)
    actions = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'NPC'
        verbose_name_plural = 'NPCs'

    def get_absolute_url(self):
        return reverse('characters:npc_detail', kwargs={
            'npc_pk': self.pk
            })


class Player(Character):
    character_name = models.CharField(max_length=255, default='')
    proficiency_bonus = models.CharField(max_length=255, default='', blank=True)
    player_name = models.CharField(max_length=255, default='', blank=True)
    character_class = models.CharField(max_length=255, default='', blank=True)
    race = models.CharField(max_length=255, default='', blank=True)
    xp = models.IntegerField(verbose_name= _('XP'), default=0, blank=True)
    background = models.CharField(max_length=255, default='', blank=True)
    age = models.CharField(max_length=255, default='', blank=True)
    height = models.CharField(max_length=255, default='', blank=True)
    weight = models.CharField(max_length=255, default='', blank=True)
    initiative = models.CharField(max_length=255, default='', blank=True)
    personality = models.TextField(blank=True)
    bonds = models.TextField(blank=True)
    ideals = models.TextField(blank=True)
    flaws = models.TextField(blank=True)
    feats = models.TextField(blank=True)
    attacks = models.TextField(blank=True)
    spells = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    traits = models.TextField(blank=True)
    proficiencies = models.TextField(blank=True)
    senses = models.CharField(max_length=255, default='', blank=True)
    equipment = models.TextField(blank=True)




    def get_absolute_url(self):
        return reverse('characters:player_detail', kwargs={
            'player_pk': self.pk
            })
    
