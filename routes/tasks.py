import asyncio
from django.db import close_old_connections
from routes.models import Assignment, AssignmentDocument


async def generate_assignment_document(assignment_id):
    await asyncio.sleep(5)

    await asyncio.get_event_loop().run_in_executor(
        None,
        _create_document,
        assignment_id
    )


def _create_document(assignment_id):
    close_old_connections()
    assignment = Assignment.objects.get(pk=assignment_id)

    if not hasattr(assignment, 'document'):
        AssignmentDocument.objects.create(assignment=assignment)