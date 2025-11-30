from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging_config import get_logger
from app.exceptions.user import ValidationError, UserNotFoundError
from app.models.candidates import Candidate
from app.models.election import Election
from app.repository.candidate_repository import CandidateRepository
from app.repository.election_repository import ElectionRepository
from app.schemas.candidate import CandidateResponse
from app.schemas.election import ElectionCreate, ElectionUpdate, ElectionResponse

logger = get_logger("election_service")


class ElectionService:
    """Service for election CRUD operations."""

    @staticmethod
    async def create_election(
        session: AsyncSession, election_data: ElectionCreate
    ) -> ElectionResponse:
        """Create a new election with candidates."""
        logger.info(f"Creating election: {election_data.title}")

        if not election_data.candidates or len(election_data.candidates) < 2:
            logger.warning("Attempt to create election without candidates")
            raise ValidationError("Election must have at least two candidates")

        repository = ElectionRepository(session)

        new_election = Election(
            title=election_data.title,
            description=election_data.description,
            start_date=election_data.start_date,
            end_date=election_data.end_date,
            is_public=election_data.is_public,
            created_at=datetime.now(timezone.utc),
        )

        created_election = await repository.create(new_election)
        logger.info(f"Election created successfully with id: {created_election.id}")

        candidate_repo = CandidateRepository(session)

        for candidate_data in election_data.candidates:
            new_candidate = Candidate(
                election_id=created_election.id,
                name=candidate_data.name,
                description=candidate_data.description,
            )
            await candidate_repo.create(new_candidate)

        logger.info(
            f"Created {len(election_data.candidates)} candidates for election {created_election.id}"
        )

        await session.refresh(created_election)

        return await ElectionService._build_election_response(
            session, created_election
        )

    @staticmethod
    async def get_election_by_id(
        session: AsyncSession, election_id: str
    ) -> Optional[ElectionResponse]:
        """Get election by ID."""
        logger.info(f"Getting election by id: {election_id}")

        repository = ElectionRepository(session)
        election = await repository.read_one(condition=Election.id == election_id)

        if not election:
            logger.warning(f"Election with id {election_id} not found")
            return None

        return await ElectionService._build_election_response(session, election)

    @staticmethod
    async def update_election(
        session: AsyncSession, election_id: str, election_data: ElectionUpdate
    ) -> ElectionResponse:
        """Update election information."""
        logger.info(f"Updating election with id: {election_id}")

        repository = ElectionRepository(session)
        election = await repository.read_one(condition=Election.id == election_id)

        if not election:
            logger.warning(f"Election with id {election_id} not found")
            raise UserNotFoundError(f"Election with id {election_id} not found")

        if election_data.candidates is not None:
            if len(election_data.candidates) < 2:
                logger.warning("Attempt to update election without candidates")
                raise ValidationError("Election must have at least two candidates")

        update_dict = election_data.model_dump(
            exclude_unset=True, exclude={"candidates"}
        )

        if update_dict:
            updated_election = await repository.update(
                data=update_dict, condition=Election.id == election_id
            )
        else:
            updated_election = election

        if election_data.candidates is not None:
            candidate_repo = CandidateRepository(session)

            existing_candidates = await candidate_repo.read_many(
                condition=Candidate.election_id == election_id
            )
            if existing_candidates:
                for candidate in existing_candidates:
                    await candidate_repo.delete(condition=Candidate.id == candidate.id)

            for candidate_data in election_data.candidates:
                new_candidate = Candidate(
                    election_id=election_id,
                    name=candidate_data.name,
                    description=candidate_data.description,
                )
                await candidate_repo.create(new_candidate)

            logger.info(
                f"Updated candidates for election {election_id}: {len(election_data.candidates)} candidates"
            )

        await session.refresh(updated_election)

        logger.info(f"Election with id {election_id} updated successfully")

        return await ElectionService._build_election_response(session, updated_election)

    @staticmethod
    async def delete_election(session: AsyncSession, election_id: str) -> bool:
        """Delete election by ID."""
        logger.info(f"Deleting election with id: {election_id}")

        repository = ElectionRepository(session)
        deleted = await repository.delete(condition=Election.id == election_id)

        if not deleted:
            logger.warning(f"Election with id {election_id} not found for deletion")
            raise UserNotFoundError(f"Election with id {election_id} not found")

        logger.info(f"Election with id {election_id} deleted successfully")
        return True

    @staticmethod
    async def get_all_elections(
        session: AsyncSession, page: int = 1, page_size: int = 10
    ) -> list[ElectionResponse]:
        """Get all elections with pagination."""
        logger.info(f"Getting all elections - page: {page}, page_size: {page_size}")

        repository = ElectionRepository(session)
        elections = await repository.read_paginated(
            condition=True, page=page, page_size=page_size
        )

        if not elections:
            return []

        result = []
        for election in elections:
            response = await ElectionService._build_election_response(session, election)
            result.append(response)

        return result

    @staticmethod
    async def _build_election_response(
        session: AsyncSession, election: Election
    ) -> ElectionResponse:
        """Build election response with candidates."""
        candidate_repo = CandidateRepository(session)

        candidates = await candidate_repo.read_many(
            condition=Candidate.election_id == election.id
        )

        candidate_responses = [
            CandidateResponse.model_validate(candidate) for candidate in candidates
        ]

        return ElectionResponse(
            id=election.id,
            title=election.title,
            description=election.description,
            start_date=election.start_date,
            end_date=election.end_date,
            is_public=election.is_public,
            created_at=election.created_at,
            candidates=candidate_responses,
        )


election_service = ElectionService()
