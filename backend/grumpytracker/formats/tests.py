import pytest
from formats.models import Format


@pytest.mark.django_db
class TestFormatModel:
    """
    Tests for the Format model
    """

    def test_format_simple_creation(self, single_camera, single_source):
        """
        Test basic Camera creation without an image
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            image_aspect="3:2",
            format_name="Open Gate",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        assert fmt.camera == single_camera
        assert fmt.image_format == "4.6K"
        assert fmt.image_aspect == "3:2"
        assert fmt.format_name == "Open Gate"
        assert fmt.sensor_width == 28.0
        assert fmt.sensor_height == 19.2
        assert fmt.image_width == 4608
        assert fmt.image_height == 3164
        assert fmt.codec == "ARRIRAW"
        assert fmt.source == single_source
        assert (
            fmt.make_notes
            == "4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications."
        )

        assert fmt.created_at is not None
        assert fmt.updated_at is not None

    def test_format_optional_fields(self, single_source, single_camera):
        """
        Some of our fields are optional see what happens if we skip them
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        assert fmt.image_aspect == ""
        assert fmt.format_name == ""
        assert fmt.is_anamorphic == False

    def test_format_str(self, single_camera, single_source):
        """
        The string representation of a make is its make and model
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            image_aspect="3:2",
            format_name="Open Gate",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        assert (
            str(fmt)
            == f"{fmt.camera.model} {fmt.image_format} {fmt.image_aspect} {fmt.format_name} ({fmt.image_width} x {fmt.image_height} ) {'Anamorphic' if fmt.is_anamorphic else ''} {fmt.pixel_aspect if fmt.pixel_aspect != 1.0 else ''}"
        )

    def test_audit_fields(self, single_camera, single_source):
        """
        We auto update audit fields on creation
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            image_aspect="3:2",
            format_name="Open Gate",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        assert fmt.created_at is not None
        assert fmt.updated_at is not None

        # Update the make
        original_updated_at = fmt.updated_at
        fmt.image_format = "4.6K U"
        fmt.save()

        assert fmt.updated_at > original_updated_at

    def test_as_dict(self, single_camera, single_source):
        """
        Does as_dict return the right fields?

        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            image_aspect="3:2",
            format_name="Open Gate",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        result = fmt.as_dict()

        expected_keys = {
            "id",
            "camera",
            "camera_model",
            "make_name",
            "source",
            "image_format",
            "image_aspect",
            "format_name",
            "sensor_width",
            "sensor_height",
            "image_width",
            "image_height",
            "is_anamorphic",
            "is_desqueezed",
            "pixel_aspect",
            "anamorphic_squeeze",
            "filmback_width_3de",
            "filmback_height_3de",
            "distortion_model_3de",
            "is_downsampled",
            "is_upscaled",
            "codec",
            "raw_recording_available",
            "notes",
            "make_notes",
            "tracking_workflow",
        }

        assert set(result.keys()) == expected_keys
        assert result["id"] == fmt.id
        assert result["camera"] == single_camera.id
        assert result["camera_model"] == single_camera.model
        assert result["make_name"] == single_camera.make.name
        assert result["source"] == single_source.id
        assert result["image_format"] == fmt.image_format
        assert result["image_aspect"] == fmt.image_aspect
        assert result["format_name"] == fmt.format_name
        assert result["sensor_width"] == fmt.sensor_width
        assert result["sensor_height"] == fmt.sensor_height
        assert result["image_width"] == fmt.image_width
        assert result["image_height"] == fmt.image_height
        assert result["is_anamorphic"] == fmt.is_anamorphic
        assert result["is_desqueezed"] == fmt.is_desqueezed
        assert result["pixel_aspect"] == fmt.pixel_aspect
        assert result["filmback_width_3de"] == fmt.filmback_width_3de
        assert result["filmback_height_3de"] == fmt.filmback_height_3de
        assert result["distortion_model_3de"] == fmt.distortion_model_3de
        assert result["is_downsampled"] == fmt.is_downsampled
        assert result["is_upscaled"] == fmt.is_upscaled
        assert result["codec"] == fmt.codec
        assert result["raw_recording_available"] == fmt.raw_recording_available
        assert result["notes"] == fmt.notes
        assert result["make_notes"] == fmt.make_notes
        assert result["tracking_workflow"] == fmt.tracking_workflow

    def test_format_search(self, single_camera, single_source):
        """
        We have a special field that combines image format, aspect and name for easy searching
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            image_aspect="3:2",
            format_name="Open Gate",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        assert fmt.format_search == "4.6K 3:2 Open Gate"

    def test_format_search_no_image_aspect(self, single_camera, single_source):
        """
        We have a special field that combines image format, aspect and name for easy searching
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            format_name="Open Gate",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        assert fmt.format_search == "4.6K Open Gate"

    def test_format_search_no_format_name(self, single_camera, single_source):
        """
        We have a special field that combines image format, aspect and name for easy searching
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            image_aspect="3:2",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        assert fmt.format_search == "4.6K 3:2"

    def test_format_search_format_only(self, single_camera, single_source):
        """
        We have a special field that combines image format, aspect and name for easy searching
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        assert fmt.format_search == "4.6K"

    def test_no_spherical_adjustment(self, single_camera, single_source):
        """
        If a format is spherical and both the image aspect and the filmback aspect match 1.0 we can use the original sensor size in 3de
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="6K",
            image_aspect="16:9",
            sensor_width=25.34,
            sensor_height=14.26,
            image_width=5760,
            image_height=3240,
            codec="R3D",
            source=single_source,
        )

        # The height of the filmback should have been edited
        assert fmt.filmback_width_3de == 25.34
        assert fmt.filmback_height_3de == 14.26

        # The recomended distortion model should be standard radial
        assert fmt.distortion_model_3de == "Radial Standard Degree 4"
        assert fmt.tracking_workflow is None

    def test_spherical_adjustment(self, single_camera, single_source):
        """
        If a format is spherical but the image aspect does not match the filmback aspect we need to correct the filmback to force
        a pixel aspect of 1.0
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="4.6K",
            image_aspect="3:2",
            format_name="Open Gate",
            sensor_width=28.0,
            sensor_height=19.2,
            image_width=4608,
            image_height=3164,
            codec="ARRIRAW",
            source=single_source,
            make_notes="4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        )

        # The height of the filmback should have been edited
        assert fmt.filmback_width_3de == 28.0
        assert fmt.filmback_height_3de != 19.2

        # The recomended distortion model should be standard radial
        assert fmt.distortion_model_3de == "Radial Standard Degree 4"
        assert (
            "ensure a pixel aspect ratio of exactly 1.0 in 3DE" in fmt.tracking_workflow
        )

    def test_is_anamorphic(self, single_camera, single_source):
        """
        Anamorphic shots that have been desqueezed in camera need a special tracking workflow
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="2.7K",
            image_aspect="8:9",
            sensor_width=16.7,
            sensor_height=18.8,
            image_width=2743,
            image_height=3086,
            codec="ARRIRAW",
            is_anamorphic=True,
            pixel_aspect=2.0,
            source=single_source,
            make_notes="For projects shooting with 2x anamorphic lenses for a target deliverable of 16:9, fulfilling 4K mandates. Desqueeze applied in-camera.",
        )

        # The width of the filmback should have been edited
        assert fmt.filmback_width_3de != 16.7
        assert fmt.filmback_height_3de == 18.8

        # The recomended distortion model should be standard anamorphic
        assert fmt.distortion_model_3de == "Anamorphic Standard Degree 4"
        assert fmt.tracking_workflow is None

    def test_is_anamorphic_and_desqueezed(self, single_camera, single_source):
        """
        Anamorphic shots that have been desqueezed in camera need a special tracking workflow
        """
        fmt = Format.objects.create(
            camera=single_camera,
            image_format="3.8K",
            image_aspect="2:1",
            format_name="Ana. 2X",
            sensor_width=18.7,
            sensor_height=18.7,
            image_width=3840,
            image_height=1920,
            codec="ProRes",
            is_anamorphic=True,
            is_desqueezed=True,
            pixel_aspect=2.0,
            source=single_source,
            notes="Dezqueezed from 3K 1:1",
            make_notes="3K 1:1 was designed for shooting with 2x anamorphic lenses for a target deliverable of 2:1, fulfilling 4K mandates.",
        )

        assert fmt.distortion_model_3de == "Anamorphic Rescaled Degree 4"
        assert "desqueezed in-camera" in fmt.tracking_workflow
