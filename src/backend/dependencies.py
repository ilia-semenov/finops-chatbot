"""Request context utilities for role enforcement."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Header

ACCESS_HIERARCHY = {
    "public": 0,
    "member": 1,
    "internal": 2,
    "confidential": 3,
}


@dataclass
class RequestContext:
    user_id: str
    role: str

    def clearance(self) -> int:
        return ACCESS_HIERARCHY.get(self.role, -1)

    def is_authorized_for(self, requested_tier: str) -> bool:
        return self.clearance() >= ACCESS_HIERARCHY.get(requested_tier, 99)


def get_request_context(
    x_user_id: str = Header("anonymous", alias="x-user-id"),
    x_user_role: str = Header("public", alias="x-user-role"),
) -> RequestContext:
    """Construct RequestContext from headers set by API gateway."""

    return RequestContext(user_id=x_user_id, role=x_user_role)
