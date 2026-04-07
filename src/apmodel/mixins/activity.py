from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apmodel.activity import Accept, Reject
    from apmodel.core import Activity
    from apmodel.objects import Actor


class ActivityMixin:
    def accept(self: "Activity", id: str, actor: "Actor") -> "Accept":
        from apmodel.activity.accept import Accept

        return Accept(id=id, actor=actor, object=self)

    def reject(self: "Activity", id: str, actor: "Actor") -> "Reject":
        from apmodel.activity.reject import Reject

        return Reject(id=id, actor=actor, object=self)
