from dataclasses import dataclass
from typing import Dict


@dataclass
class ToothAnalyzeDto:
    ImageData: str = ""
    AnalysisResult: str = ""
