import pytest
from datetime import date
from django.db import IntegrityError
from projects.models import Project, ProjectFormat, Vote


@pytest.mark.django_db
class TestProjectModel:
    """
    Tests for the Project model
    """

    def test_project_simple_creation(self):
        """
        Test basic Project creation with required fields
        """
        project = Project.objects.create(
            name="Test Movie",
            project_type="feature",
            description="A test movie for our test suite",
            release_date=date(2024, 1, 1),
        )

        assert project.name == "Test Movie"
        assert project.project_type == "feature"
        assert project.description == "A test movie for our test suite"
        assert project.release_date == date(2024, 1, 1)
        assert project.adult is False
        assert project.url is None
        assert project.poster_path is None
        assert project.tmdb_id is None
        assert project.tmdb_original_name is None
        assert project.genres == []  # Default empty list
        assert project.rating == []  # Default empty list

    def test_project_type_choices(self):
        """
        Test that project_type accepts valid choices and defaults correctly
        """
        # Test feature type
        feature_project = Project.objects.create(
            name="Feature Film", project_type="feature"
        )
        assert feature_project.project_type == "feature"

        # Test episodic type
        episodic_project = Project.objects.create(
            name="TV Series", project_type="episodic"
        )
        assert episodic_project.project_type == "episodic"

        # Test default value
        default_project = Project.objects.create(name="Default Project")
        assert default_project.project_type == "feature"

    def test_as_dict(self):
        """
        Test the as_dict method returns the correct fields
        """
        project = Project.objects.create(
            name="Dict Test Movie",
            url="https://example.com/dict-test",
            project_type="episodic",
            description="Testing as_dict method",
            poster_path="/dict/poster.jpg",
            release_date=date(2024, 3, 10),
            adult=True,
            tmdb_id=98765,
            tmdb_original_name="Dict Test Original",
            genres=["Comedy", "Sci-Fi"],
            rating=[{"source": "RT", "rating": "95%"}],
        )

        result = project.as_dict()

        expected_keys = {
            "id",
            "name",
            "project_type",
            "description",
            "poster_path",
            "release_date",
            "adult",
            "tmdb_id",
            "tmdb_original_name",
            "genres",
            "rating",
        }

        assert set(result.keys()) == expected_keys
        assert result["id"] == project.id
        assert result["name"] == "Dict Test Movie"
        assert result["project_type"] == "episodic"
        assert result["description"] == "Testing as_dict method"
        assert result["poster_path"] == "/dict/poster.jpg"
        assert result["release_date"] == date(2024, 3, 10)
        assert result["adult"] is True
        assert result["tmdb_id"] == 98765
        assert result["tmdb_original_name"] == "Dict Test Original"
        assert result["genres"] == ["Comedy", "Sci-Fi"]
        assert result["rating"] == [{"source": "RT", "rating": "95%"}]

    def test_project_cameras_relationship(self, multiple_cameras):
        """
        Test the many-to-many relationship with cameras
        """
        project = Project.objects.create(name="Camera Test Project")

        # Add cameras to the project
        project.cameras.add(multiple_cameras[0])
        project.cameras.add(multiple_cameras[1])

        assert project.cameras.count() == 2
        assert multiple_cameras[0] in project.cameras.all()
        assert multiple_cameras[1] in project.cameras.all()

        # Test reverse relationship
        assert project in multiple_cameras[0].used_in_projects.all()
        assert project in multiple_cameras[1].used_in_projects.all()

    def test_with_formats_no_formats(self, single_user):
        """
        Test the with_formats method when project has no formats
        """
        project = Project.objects.create(name="No Formats Project")

        result = project.with_formats(user=single_user)

        # Should include all as_dict fields plus cameras and formats
        expected_keys = {
            "id",
            "name",
            "project_type",
            "description",
            "poster_path",
            "release_date",
            "adult",
            "tmdb_id",
            "tmdb_original_name",
            "genres",
            "rating",
            "cameras",
            "formats",
        }

        assert set(result.keys()) == expected_keys
        assert result["cameras"] == []
        assert result["formats"] == []

    def test_with_formats_with_formats_no_votes(
        self, single_format, single_camera, single_user
    ):
        """
        Test the with_formats method when project has formats but no votes
        """
        project = Project.objects.create(name="Formats No Votes Project")
        project.cameras.add(single_camera)

        # Create ProjectFormat relationship
        ProjectFormat.objects.create(
            project=project, fmt=single_format, added_by=single_user
        )

        result = project.with_formats(user=single_user)

        assert len(result["cameras"]) == 1
        assert len(result["formats"]) == 1

        format_data = result["formats"][0]
        assert format_data["up_votes"] == 0
        assert format_data["down_votes"] == 0
        assert format_data["total_votes"] == 0
        assert format_data["score"] == 0
        assert format_data["user_vote"] is None

    def test_with_formats_and_votes(self, single_format, single_user, multiple_users):
        """
        Test the with_formats method when project has formats with votes
        """
        project = Project.objects.create(name="Formats With Votes Project")

        # Create ProjectFormat relationship
        ProjectFormat.objects.create(
            project=project, fmt=single_format, added_by=single_user
        )

        # Create votes
        Vote.objects.create(
            project=project, fmt=single_format, user=single_user, vote_type="up"
        )
        Vote.objects.create(
            project=project, fmt=single_format, user=multiple_users[0], vote_type="up"
        )
        Vote.objects.create(
            project=project, fmt=single_format, user=multiple_users[1], vote_type="down"
        )

        # Test with the user who voted
        result = project.with_formats(user=single_user)
        format_data = result["formats"][0]

        assert format_data["up_votes"] == 2
        assert format_data["down_votes"] == 1
        assert format_data["total_votes"] == 3
        assert format_data["score"] == 1  # 2 up - 1 down
        assert format_data["user_vote"] == "up"

        # Test with a user who didn't vote
        result_no_vote = project.with_formats(user=multiple_users[2])
        format_data_no_vote = result_no_vote["formats"][0]
        assert format_data_no_vote["user_vote"] is None

        # Test without specifying a user
        result_no_user = project.with_formats()
        format_data_no_user = result_no_user["formats"][0]
        assert format_data_no_user["user_vote"] is None


@pytest.mark.django_db
class TestProjectFormatModel:
    """
    Tests for the ProjectFormat through model
    """

    def test_project_format_creation(self, single_format, single_user):
        """
        Test basic ProjectFormat creation
        """
        project = Project.objects.create(name="ProjectFormat Test")

        project_format = ProjectFormat.objects.create(
            project=project, fmt=single_format, added_by=single_user
        )

        assert project_format.project == project
        assert project_format.fmt == single_format
        assert project_format.added_by == single_user
        assert project_format.created_at is not None
        assert project_format.updated_at is not None

    def test_project_format_unique_together(self, single_format, single_user):
        """
        Project and format combination must be unique
        """
        project = Project.objects.create(name="Unique Test Project")

        # Create first ProjectFormat
        ProjectFormat.objects.create(
            project=project, fmt=single_format, added_by=single_user
        )

        # Try to create duplicate - should raise IntegrityError
        with pytest.raises(IntegrityError):
            ProjectFormat.objects.create(
                project=project, fmt=single_format, added_by=single_user
            )

    def test_project_format_optional_added_by(self, single_format):
        """
        Test that added_by field can be null (this should probably not be)
        """
        project = Project.objects.create(name="Optional User Test")

        project_format = ProjectFormat.objects.create(
            project=project, fmt=single_format
        )

        assert project_format.added_by is None


@pytest.mark.django_db
class TestVoteModel:
    """
    Tests for the Vote model
    """

    def test_up_vote(self, single_format, single_user):
        """
        Test basic Vote creation
        """
        project = Project.objects.create(name="Vote Test Project")

        vote = Vote.objects.create(
            project=project, fmt=single_format, user=single_user, vote_type="up"
        )

        assert vote.project == project
        assert vote.fmt == single_format
        assert vote.user == single_user
        assert vote.vote_type == "up"
        assert vote.created_at is not None

    def test_down_vote(self, single_format, single_user):
        """
        Can we down vote?
        """
        project = Project.objects.create(name="Down Vote Test")

        vote = Vote.objects.create(
            project=project, fmt=single_format, user=single_user, vote_type="down"
        )

        assert vote.vote_type == "down"

    def test_vote_unique_together(self, single_format, single_user):
        """
        The project, format, and user combination must be unique
        """
        project = Project.objects.create(name="Vote Unique Test")

        # Create first vote
        Vote.objects.create(
            project=project, fmt=single_format, user=single_user, vote_type="up"
        )

        # Try to create duplicate - should raise IntegrityError
        with pytest.raises(IntegrityError):
            Vote.objects.create(
                project=project, fmt=single_format, user=single_user, vote_type="down"
            )

    def test_vote_str(self, single_format, single_user):
        """
        The string representation of a vote has the project format user and direction
        """
        project = Project.objects.create(name="String Test Project")

        vote = Vote.objects.create(
            project=project, fmt=single_format, user=single_user, vote_type="up"
        )

        expected_str = f"<Vote Project: {project} Format: {single_format} User: {single_user} Vote: up>"
        assert str(vote) == expected_str
