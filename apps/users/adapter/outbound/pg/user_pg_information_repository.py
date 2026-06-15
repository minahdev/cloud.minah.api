import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.app.labels import (
    EXPERIENCE_LABELS,
    FAVORITE_EXERCISE_LABELS,
    GENDER_LABELS,
    WEEKLY_GOAL_LABELS,
    experience_to_code,
    experience_to_label,
    favorite_exercise_to_code,
    favorite_exercise_to_label,
    gender_to_code,
    gender_to_label,
    weekly_goal_to_code,
    weekly_goal_to_label,
)
from users.adapter.inbound.api.schemas.mypage_schema import (
    MyPageProfileResponse,
    MyPageProfileSchema,
)
from users.app.dtos.user_information_dto import UserInformation
from users.app.dtos.user_dto import User
from users.app.ports.output.mypage_repository import MyPageRepository

logger = logging.getLogger(__name__)


class UserInformationRepository(MyPageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_login_user_id(self, login_user_id: str) -> UserInformation | None:
        user_stmt = select(User).where(User.user_id == login_user_id)
        user_result = await self._session.execute(user_stmt)
        user = user_result.scalar_one_or_none()
        if user is None:
            return None

        stmt = select(UserInformation).where(UserInformation.user_id == user.id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    def _to_profile_response(
        self, row: UserInformation, login_user_id: str
    ) -> MyPageProfileResponse:
        experience_code = experience_to_code(row.exercise_experience)
        weekly_goal_code = weekly_goal_to_code(row.weekly_goal)
        favorite_code = favorite_exercise_to_code(row.favorite_exercise)
        gender_code = gender_to_code(row.gender)
        gender_api = gender_code if gender_code in GENDER_LABELS else None
        return MyPageProfileResponse(
            userId=login_user_id,
            name=row.full_name,
            gender=gender_api,
            genderLabel=GENDER_LABELS.get(gender_code or "", row.gender or ""),
            birthDate=row.birth_date,
            phone=row.phone,
            heightCm=row.height_cm,
            weightKg=row.weight_kg,
            favoriteExercise=favorite_code,
            favoriteExerciseOther=row.favorite_exercise_other or "",
            experience=experience_code,
            weeklyGoal=weekly_goal_code,
            experienceLabel=EXPERIENCE_LABELS.get(
                experience_code or "", row.exercise_experience
            ),
            weeklyGoalLabel=WEEKLY_GOAL_LABELS.get(weekly_goal_code or "", row.weekly_goal),
            favoriteExerciseLabel=FAVORITE_EXERCISE_LABELS.get(
                favorite_code or "", row.favorite_exercise
            ),
            healthNote=row.health_note or "",
        )

    async def get_profile(self, login_user_id: str) -> MyPageProfileResponse | None:
        row = await self.find_by_login_user_id(login_user_id)
        if row is None:
            return None
        return self._to_profile_response(row, login_user_id)

    async def save_profile(self, profile: MyPageProfileSchema) -> None:
        logger.info("[UserInformationRepository] save_profile | userId=%s", profile.userId)

        user_stmt = select(User).where(User.user_id == profile.userId)
        user_result = await self._session.execute(user_stmt)
        user = user_result.scalar_one_or_none()
        if user is None:
            raise ValueError("사용자를 찾을 수 없습니다.")

        row = await self.find_by_login_user_id(profile.userId)
        if row is None:
            row = UserInformation(user_id=user.id)
            self._session.add(row)

        row.full_name = profile.name
        row.gender = gender_to_label(profile.gender)
        row.birth_date = profile.birthDate
        row.phone = profile.phone
        row.height_cm = profile.heightCm
        row.weight_kg = profile.weightKg
        row.favorite_exercise = favorite_exercise_to_label(profile.favoriteExercise)
        row.favorite_exercise_other = profile.favoriteExerciseOther or None
        row.exercise_experience = experience_to_label(profile.experience)
        row.weekly_goal = weekly_goal_to_label(profile.weeklyGoal)
        row.health_note = profile.healthNote or None

        await self._session.commit()
        logger.info("[UserInformationRepository] save_profile 완료 | userId=%s", profile.userId)
