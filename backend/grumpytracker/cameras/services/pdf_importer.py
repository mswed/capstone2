import fitz
import re
from pprint import pprint
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class FormatExtractor:
    """Flexible extractor for camera formats"""

    # Common patterns to look for
    format_header_pattern: str = (
        r"^(\d+(?:\.\d+)?K\s+\d+:\d+(?:\s+(?:Open\s+Gate|S16))?)$"
    )
    dimension_pattern: str = r"(\d+\.\d+)\s*x\s*(\d+\.\d+)\s*mm"
    resolution_pattern: str = (
        r"([A-Za-z0-9\.]+(?:\s+[A-Za-z0-9\.]+)*)\s*\((\d+)\s*x\s*(\d+)\)"
    )
    circle_pattern: str = r"Image Circle [Ø]?\s*(\d+\.\d+)\s*mm"

    # Results
    formats_dict: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    current_format_name: Optional[str] = None

    def extract_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract camera formats from PDF"""
        doc = fitz.open(pdf_path)

        for page in doc:
            # Get text blocks with their positions
            blocks = page.get_text("blocks")
            blocks.sort(key=lambda b: b[1])  # Sort by top position

            # Process each block
            for block in blocks:
                text = block[4]  # Text content is at index 4

                # First check for format headers
                self.identify_format_header(text)

                # Then extract details
                if (
                    self.current_format_name
                    and self.current_format_name in self.formats_dict
                ):
                    self.extract_format_details(text)

        self.clean_formats()
        # Convert dictionary to list
        return list(self.formats_dict.values())

    def identify_format_header(self, text: str) -> None:
        """Identify if text contains a format header and set current_format_name"""
        lines = text.strip().split("\n")

        for line in lines:
            # Check for standalone format headers
            match = re.match(self.format_header_pattern, line.strip())
            if match:
                format_name = match.group(1).strip()
                if len(format_name) > 30:  # Skip if too long
                    continue

                # Create format if not exists
                if format_name not in self.formats_dict:
                    self.formats_dict[format_name] = {
                        "format_name": format_name,
                        "resolutions": [],
                    }
                self.current_format_name = format_name
                return

            # Special case for numbered format patterns (e.g., "3.3K 6:5")
            # that don't match the strict pattern above
            if re.match(r"^\d+(?:\.\d+)?K\s+\d+:\d+", line.strip()):
                format_name = line.strip().split("\n")[0]
                # Limit to the format name part only
                format_name = re.match(
                    r"(\d+(?:\.\d+)?K\s+\d+:\d+(?:\s+(?:Open\s+Gate|S16|Ana\.\s+\d+x))?)",
                    format_name,
                )
                if format_name:
                    format_name = format_name.group(1).strip()
                    if format_name not in self.formats_dict:
                        self.formats_dict[format_name] = {
                            "format_name": format_name,
                            "resolutions": [],
                        }
                    self.current_format_name = format_name
                    return

    def extract_format_details(self, text: str) -> None:
        """Extract details for the current format from text"""
        current_format = self.formats_dict[self.current_format_name]

        # Extract sensor dimensions
        dim_match = re.search(self.dimension_pattern, text)
        if dim_match and "Dimensions" in text:
            current_format["sensor_width"] = float(dim_match.group(1))
            current_format["sensor_height"] = float(dim_match.group(2))

        # Extract image circle
        circle_match = re.search(self.circle_pattern, text)
        if circle_match:
            current_format["image_circle"] = float(circle_match.group(1))

        # Extract resolutions and check for anamorphic formats
        self.extract_resolutions(text, current_format)

    def extract_resolutions(self, text: str, current_format: Dict[str, Any]) -> None:
        """Extract resolution information including special anamorphic formats"""
        # First look for standard resolutions
        resolution_matches = re.finditer(self.resolution_pattern, text)

        for match in resolution_matches:
            name = match.group(1).strip()
            width = int(match.group(2))
            height = int(match.group(3))

            # Check if this is an anamorphic format
            is_anamorphic = False
            if "Ana" in name or re.search(r"Ana\.", text):
                is_anamorphic = True

            resolution = {"name": name, "width": width, "height": height}

            if is_anamorphic:
                resolution["anamorphic"] = True

            # Add if not already in the list
            self.add_unique_resolution(current_format, resolution)

        # Special handling for lines with "Ana." that might not be captured above
        if "Ana." in text:
            # Look for anamorphic resolution pattern
            anamorphic_matches = re.finditer(
                r"(\d+(?:\.\d+)?K\s+[\d\.]+:\d+(?:\s+Ana\.\s+\d+x))\s*\((\d+)\s*x\s*(\d+)\)",
                text,
            )

            for match in anamorphic_matches:
                resolution = {
                    "name": match.group(1).strip(),
                    "width": int(match.group(2)),
                    "height": int(match.group(3)),
                    "anamorphic": True,
                }
                self.add_unique_resolution(current_format, resolution)

    def add_unique_resolution(
        self, format_data: Dict[str, Any], resolution: Dict[str, Any]
    ) -> None:
        """Add resolution if not already present"""
        if not any(
            r.get("name") == resolution["name"]
            and r.get("width") == resolution["width"]
            and r.get("height") == resolution["height"]
            for r in format_data["resolutions"]
        ):
            format_data["resolutions"].append(resolution)

    def clean_formats(self):
        """Remove formats without dimensions or resolutions"""
        formats_to_remove = []
        for name, format_data in self.formats_dict.items():
            # Remove formats without dimensions
            if "sensor_width" not in format_data:
                formats_to_remove.append(name)
            # Check for problematic formats
            elif len(name) > 30 or " was " in name:
                formats_to_remove.append(name)

        for name in formats_to_remove:
            del self.formats_dict[name]

    # Add this method to the FormatExtractor class
    def debug_anamorphic_formats(self, pdf_path):
        """Debug method to find anamorphic format text"""
        doc = fitz.open(pdf_path)

        print("=== SEARCHING FOR ANAMORPHIC FORMATS ===")
        for page in doc:
            blocks = page.get_text("blocks")
            for block in blocks:
                text = block[4]
                if "Ana" in text:
                    print("\nFOUND BLOCK WITH 'Ana':")
                    print("-" * 50)
                    print(text)
                    print("-" * 50)

                    # Try to extract with regex
                    ana_matches = re.finditer(
                        r"(\d+(?:\.\d+)?K\s+[\d\.]+:\d+(?:\s+Ana\.\s+\d+x))\s*\((\d+)\s*x\s*(\d+)\)",
                        text,
                    )
                    for match in ana_matches:
                        print(
                            f"MATCH: {match.group(1)} ({match.group(2)}x{match.group(3)})"
                        )


# Usage
extractor = FormatExtractor()
formats = extractor.extract_from_pdf(
    "/home/mswed/Documents/coding/springboard/capstone2/backend/grumpytracker/cameras/ALEXA 35 _ ALEXA 35 Live.pdf"
)
pprint(formats)
# Run the debug function
extractor.debug_anamorphic_formats(
    "/home/mswed/Documents/coding/springboard/capstone2/backend/grumpytracker/cameras/ALEXA 35 _ ALEXA 35 Live.pdf"
)
