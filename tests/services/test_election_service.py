from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.exceptions.user import UserNotFoundError, ValidationError
from app.schemas.attachment import AttachmentCreate
from app.schemas.candidate import CandidateCreate
from app.schemas.election import ElectionCreate, ElectionUpdate
from app.schemas.election_setting import ElectionSettingBase
from app.services.election import ElectionService


@pytest.mark.asyncio
async def test_create_election_success(async_session_mock):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    election_data = ElectionCreate(
        title="Test election",
        description="Desc",
        start_date=now,
        end_date=now,
        is_public=True,
        candidates=[
            CandidateCreate(name="A", description=None),
            CandidateCreate(name="B", description=None),
        ],
        settings=ElectionSettingBase(
            allow_revoting=True,
            max_votes=1,
            require_auth=True,
        ),
        attachments=[
            AttachmentCreate(file_url="http://file.pdf"),
        ],
    )

    created_election = SimpleNamespace(
        id="election-id-1",
        title=election_data.title,
        description=election_data.description,
        start_date=election_data.start_date,
        end_date=election_data.end_date,
        is_public=election_data.is_public,
        created_at=now,
    )

    with patch(
        "app.services.election.ElectionRepository"
    ) as election_repo_cls, patch(
        "app.services.election.ElectionSettingRepository"
    ) as setting_repo_cls, patch(
        "app.services.election.CandidateRepository"
    ) as candidate_repo_cls, patch(
        "app.services.election.AttachmentRepository"
    ) as attachment_repo_cls:
        election_repo = AsyncMock()
        election_repo.create.return_value = created_election
        election_repo_cls.return_value = election_repo

        setting_repo = AsyncMock()
        setting_repo.create.return_value = None
        setting_repo.read_one.return_value = SimpleNamespace(
            id="setting-id-1",
            election_id=created_election.id,
            allow_revoting=True,
            max_votes=1,
            require_auth=True,
        )
        setting_repo_cls.return_value = setting_repo

        candidate_repo = AsyncMock()
        candidate_repo.create.return_value = None
        candidate_repo.read_many.return_value = [
            SimpleNamespace(
                id="cand-1",
                election_id=created_election.id,
                name="A",
                description=None,
            ),
            SimpleNamespace(
                id="cand-2",
                election_id=created_election.id,
                name="B",
                description=None,
            ),
        ]
        candidate_repo_cls.return_value = candidate_repo

        attachment_repo = AsyncMock()
        attachment_repo.create.return_value = None
        attachment_repo.read_many.return_value = [
            SimpleNamespace(
                id="att-1",
                election_id=created_election.id,
                file_url="http://file.pdf",
                uploaded_at=now,
            )
        ]
        attachment_repo_cls.return_value = attachment_repo

        async_session_mock.refresh = AsyncMock()

        result = await ElectionService.create_election(async_session_mock, election_data)

        assert result.id == created_election.id
        assert len(result.candidates) == 2
        assert result.settings is not None
        assert len(result.attachments) == 1


@pytest.mark.asyncio
async def test_create_election_not_enough_candidates(async_session_mock):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    # Создаём модель ElectionCreate без валидации, чтобы обойти min_items=2
    election_data = ElectionCreate.model_construct(
        title="Test election",
        description="Desc",
        start_date=now,
        end_date=now,
        is_public=True,
        candidates=[CandidateCreate(name="Only", description=None)],
        settings=None,
        attachments=None,
    )

    with pytest.raises(ValidationError):
        await ElectionService.create_election(async_session_mock, election_data)


@pytest.mark.asyncio
async def test_get_election_by_id_not_found(async_session_mock):
    with patch("app.services.election.ElectionRepository") as election_repo_cls:
        election_repo = AsyncMock()
        election_repo.read_one.return_value = None
        election_repo_cls.return_value = election_repo

        result = await ElectionService.get_election_by_id(
            async_session_mock, "missing-id"
        )

        assert result is None
        election_repo.read_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_election_not_found(async_session_mock):
    update_data = ElectionUpdate(title="New title")

    with patch("app.services.election.ElectionRepository") as election_repo_cls:
        election_repo = AsyncMock()
        election_repo.read_one.return_value = None
        election_repo_cls.return_value = election_repo

        with pytest.raises(UserNotFoundError):
            await ElectionService.update_election(
                async_session_mock, "missing-id", update_data
            )


@pytest.mark.asyncio
async def test_update_election_not_enough_candidates(async_session_mock):
    # Аналогично, создаём ElectionUpdate без валидации с 1 кандидатом
    update_data = ElectionUpdate.model_construct(
        candidates=[CandidateCreate(name="Only", description=None)]
    )

    with patch("app.services.election.ElectionRepository") as election_repo_cls:
        election_repo = AsyncMock()
        election_repo.read_one.return_value = SimpleNamespace(id="election-id-1")
        election_repo_cls.return_value = election_repo

        with pytest.raises(ValidationError):
            await ElectionService.update_election(
                async_session_mock, "election-id-1", update_data
            )


@pytest.mark.asyncio
async def test_delete_election_success(async_session_mock):
    with patch("app.services.election.ElectionRepository") as election_repo_cls:
        election_repo = AsyncMock()
        election_repo.delete.return_value = True
        election_repo_cls.return_value = election_repo

        result = await ElectionService.delete_election(
            async_session_mock, "election-id-1"
        )

        assert result is True
        election_repo.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_election_not_found(async_session_mock):
    with patch("app.services.election.ElectionRepository") as election_repo_cls:
        election_repo = AsyncMock()
        election_repo.delete.return_value = False
        election_repo_cls.return_value = election_repo

        with pytest.raises(UserNotFoundError):
            await ElectionService.delete_election(
                async_session_mock, "missing-id"
            )


