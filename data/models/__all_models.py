from data.models.auth_sessions import Session
from data.models.habits_notes import HabitNote
from data.models.mood_notes import MoodNote
from data.models.mood_scales import MoodScale
from data.models.test_results import TestResult
from data.models.text_data import Result
from data.models.users import User

MODELS_STRINGS = ["Session", "Habit", "MoodNote", "MoodScale", "TestResult", "Result", "User"]
MODELS = [Session, HabitNote, MoodNote, MoodScale, TestResult, Result, User]
