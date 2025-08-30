from django.db import models

# Create your models here.

class TitleBasics(models.Model):

    # tconst: Unique title ID (e.g. tt0111161)
    # titleType: Format (movie, short, tvSeries, tvEpisode, video, etc.)
    # primaryTitle: Popular title used in promotional materials
    # originalTitle: Original language title
    # isAdult: 0 = non-adult, 1 = adult
    # startYear: Release year (YYYY or \N)
    # endYear: End year for series (YYYY or \N)
    # runtimeMinutes: Duration in minutes (\N if unknown)
    # genres: Comma-separated genres (e.g. Comedy,Drama)

    tconst = models.CharField(max_length=20, primary_key=True)
    title_type = models.CharField(max_length=20, db_index=True)
    primary_title = models.CharField(max_length=500, db_index=True)
    original_title = models.CharField(max_length=500, db_index=True)
    is_adult = models.BooleanField()
    start_year = models.IntegerField(null=True, blank=True, db_index=True)
    end_year = models.IntegerField(null=True, blank=True)
    runtime_minutes = models.IntegerField(null=True, blank=True)
    genres = models.CharField(max_length=100, db_index=True)


class NameBasics(models.Model):

    # nconst: Unique person identifier (e.g. nm0000001)
    # primaryName: The credited name (e.g., "Brad Pitt")
    # birthYear: Year of birth (YYYY or \N)
    # deathYear: Year of death (YYYY or \N)
    # primaryProfession: Top professions (e.g., “actor,director”)
    # knownForTitles: Titles the person is well known for (tconst list)

    nconst = models.CharField(max_length=20, primary_key=True)
    primary_name = models.CharField(max_length=255, db_index=True)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    primary_profession = models.CharField(max_length=255, null=True, db_index=True)
    known_for_titles = models.CharField(max_length=500, null=True, db_index=True)  # Can be split later


class TitleCrew(models.Model):

    # tconst: Links to title
    # directors: Comma-separated nconst values
    # writers: Comma-separated nconst values

    tconst = models.OneToOneField(TitleBasics, on_delete=models.CASCADE, primary_key=True)
    directors = models.ManyToManyField(NameBasics, related_name='directed_titles')
    writers = models.ManyToManyField(NameBasics, related_name='written_titles')


class TitleRatings(models.Model):

    # tconst: Title ID
    # averageRating: Weighted average rating
    # numVotes: Total number of user votes

    tconst = models.OneToOneField(TitleBasics, on_delete=models.CASCADE, primary_key=True)
    average_rating = models.FloatField()
    num_votes = models.IntegerField()


class TitleAkas(models.Model):

    # titleId: Title ID→ Refers to the main title in TitleBasics (foreign key relationship).
    # ordering: Display order→ Integer used to order multiple alternate titles for the same title.
    # title: Localized or alternate title→ The alternate name used in a specific region/language.
    # region: Geographic region→ Country or region where the alternate title is used (e.g., US, IN).
    # language: Language code→ ISO 639-1 or ISO 639-2 code of the language (e.g., en, hi).
    # types: Type of alternate title→ Describes the reason/type (e.g., “original”, “alternative”, “dvd”, “festival”).
    # attributes: Additional info→ Contextual attributes like “IMAX”, “3D”, etc. (can be null).
    # isOriginalTitle: Original title flag→ Boolean (0 or 1). 1 indicates this is the original title used in that region/language.

    tconst = models.ForeignKey(TitleBasics, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    title_text = models.CharField(max_length=500)
    region = models.CharField(max_length=20, null=True)
    language = models.CharField(max_length=20, null=True)
    types = models.CharField(max_length=100, null=True)
    attributes = models.CharField(max_length=100, null=True)
    is_original_title = models.BooleanField(null=True)


class TitleEpisode(models.Model):

    # tconst: Episode's own title ID
    # parentTconst: Parent TV series title ID
    # seasonNumber: Season number (\N if unavailable)
    # episodeNumber: Episode number in that season (\N if unavailable)

    tconst = models.OneToOneField(TitleBasics, on_delete=models.CASCADE, primary_key=True)
    parent = models.ForeignKey(TitleBasics, on_delete=models.CASCADE, related_name='episodes')
    season_number = models.IntegerField(null=True)
    episode_number = models.IntegerField(null=True)


class TitlePrincipals(models.Model):

    # tconst: Title ID
    # ordering: Row order for that title
    # nconst: Person ID
    # category: Role category (actor, director, self, etc.)
    # job: Specific job title, if available (or \N)
    # characters: Character names portrayed (e.g. ["John Doe"], or \N)

    tconst = models.ForeignKey(TitleBasics, on_delete=models.CASCADE)
    nconst = models.ForeignKey(NameBasics, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    category = models.CharField(max_length=100)
    job = models.CharField(max_length=255, null=True)
    characters = models.CharField(max_length=500, null=True)
