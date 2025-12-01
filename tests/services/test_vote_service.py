from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.exceptions.user import PermissionDeniedError, VoteNotFoundError
from app.models.user import User
from app.schemas.vote import VoteCreate, VoteUpdate
from app.services.vote import VoteService


@pytest.mark.asyncio
async def test_create_vote_success(async_session_mock):
    vote_data = VoteCreate(
        election_id="election-id-1",
        candidate_id="candidate-id-1",
    )
    current_user = SimpleNamespace(id="user-id-1")

    created_vote = SimpleNamespace(
        id="vote-id-1",
        election_id=vote_data.election_id,
        voter_id=current_user.id,
        candidate_id=vote_data.candidate_id,
    )

    with patch("app.services.vote.VoteRepository") as vote_repo_cls:
        vote_repo = AsyncMock()
        vote_repo.create.return_value = created_vote
        vote_repo_cls.return_value = vote_repo

        result = await VoteService.create_vote(async_session_mock, vote_data, current_user)

        assert result.id == created_vote.id
        assert result.election_id == vote_data.election_id
        vote_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_vote_by_id_not_found(async_session_mock):
    with patch("app.services.vote.VoteRepository") as vote_repo_cls:
        vote_repo = AsyncMock()
        vote_repo.read_one.return_value = None
        vote_repo_cls.return_value = vote_repo

        result = await VoteService.get_vote_by_id(async_session_mock, "missing-id")

        assert result is None
        vote_repo.read_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_vote_success(async_session_mock):
    vote_id = "vote-id-1"
    existing_vote = SimpleNamespace(
        id=vote_id,
        election_id="election-id-1",
        voter_id="user-id-1",
        candidate_id="candidate-id-1",
    )
    updated_vote = SimpleNamespace(
        id=vote_id,
        election_id="election-id-1",
        voter_id="user-id-1",
        candidate_id="candidate-id-2",
    )
    current_user = SimpleNamespace(id="user-id-1")
    update_data = VoteUpdate(candidate_id="candidate-id-2")

    with patch("app.services.vote.VoteRepository") as vote_repo_cls:
        vote_repo = AsyncMock()
        vote_repo.read_one.return_value = existing_vote
        vote_repo.update.return_value = updated_vote
        vote_repo_cls.return_value = vote_repo

        result = await VoteService.update_vote(
            async_session_mock, vote_id, update_data, current_user
        )

        assert result.candidate_id == update_data.candidate_id
        vote_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_vote_not_found(async_session_mock):
    vote_id = "missing-id"
    current_user = SimpleNamespace(id="user-id-1")
    update_data = VoteUpdate(candidate_id="candidate-id-2")

    with patch("app.services.vote.VoteRepository") as vote_repo_cls:
        vote_repo = AsyncMock()
        vote_repo.read_one.return_value = None
        vote_repo_cls.return_value = vote_repo

        with pytest.raises(VoteNotFoundError):
            await VoteService.update_vote(
                async_session_mock, vote_id, update_data, current_user
            )


@pytest.mark.asyncio
async def test_update_vote_permission_denied(async_session_mock):
    vote_id = "vote-id-1"
    existing_vote = SimpleNamespace(
        id=vote_id,
        election_id="election-id-1",
        voter_id="another-user",
        candidate_id="candidate-id-1",
    )
    current_user = SimpleNamespace(id="user-id-1")
    update_data = VoteUpdate(candidate_id="candidate-id-2")

    with patch("app.services.vote.VoteRepository") as vote_repo_cls:
        vote_repo = AsyncMock()
        vote_repo.read_one.return_value = existing_vote
        vote_repo_cls.return_value = vote_repo

        with pytest.raises(PermissionDeniedError):
            await VoteService.update_vote(
                async_session_mock, vote_id, update_data, current_user
            )


@pytest.mark.asyncio
async def test_delete_vote_success(async_session_mock):
    vote_id = "vote-id-1"
    existing_vote = SimpleNamespace(
        id=vote_id,
        election_id="election-id-1",
        voter_id="user-id-1",
        candidate_id="candidate-id-1",
    )
    current_user = SimpleNamespace(id="user-id-1")

    with patch("app.services.vote.VoteRepository") as vote_repo_cls:
        vote_repo = AsyncMock()
        vote_repo.read_one.return_value = existing_vote
        vote_repo.delete.return_value = True
        vote_repo_cls.return_value = vote_repo

        result = await VoteService.delete_vote(
            async_session_mock, vote_id, current_user
        )

        assert result is True
        vote_repo.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_vote_not_found(async_session_mock):
    vote_id = "missing-id"
    current_user = SimpleNamespace(id="user-id-1")

    with patch("app.services.vote.VoteRepository") as vote_repo_cls:
        vote_repo = AsyncMock()
        vote_repo.read_one.return_value = None
        vote_repo_cls.return_value = vote_repo

        with pytest.raises(VoteNotFoundError):
            await VoteService.delete_vote(
                async_session_mock, vote_id, current_user
            )


@pytest.mark.asyncio
async def test_delete_vote_permission_denied(async_session_mock):
    vote_id = "vote-id-1"
    existing_vote = SimpleNamespace(
        id=vote_id,
        election_id="election-id-1",
        voter_id="another-user",
        candidate_id="candidate-id-1",
    )
    current_user = SimpleNamespace(id="user-id-1")

    with patch("app.services.vote.VoteRepository") as vote_repo_cls:
        vote_repo = AsyncMock()
        vote_repo.read_one.return_value = existing_vote
        vote_repo.delete.return_value = False
        vote_repo_cls.return_value = vote_repo

        with pytest.raises(PermissionDeniedError):
            await VoteService.delete_vote(
                async_session_mock, vote_id, current_user
            )


