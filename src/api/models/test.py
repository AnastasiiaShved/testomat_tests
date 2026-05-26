from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TestAttributes(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    title: str = ""
    state: str = "manual"
    suite_id: str | None = Field(default=None, alias="suite-id")
    description: str | None = None
    priority: str | None = None
    sync: bool = True
    tags: list[str] = Field(default_factory=list)
    code: str | None = None
    file: str | None = None
    emoji: Any | None = None
    recordings_count: int | None = Field(default=None, alias="recordings-count")
    last_sync_id: str | None = Field(default=None, alias="last-sync-id")
    run_statuses: list[Any] = Field(default_factory=list, alias="run-statuses")
    assigned_to: str | None = Field(default=None, alias="assigned-to")
    has_examples: Any | None = Field(default=None, alias="has-examples")
    params: list[Any] = Field(default_factory=list)
    public_title: str | None = Field(default=None, alias="public-title")
    previous_description: str | None = Field(default=None, alias="previous-description")
    import_id: str | None = Field(default=None, alias="import-id")
    play_url: str | None = Field(default=None, alias="play-url")
    jira_issues: Any | None = Field(default=None, alias="jira-issues")
    attachments: Any | None = None


class Test(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: str = "test"
    attributes: TestAttributes = Field(default_factory=TestAttributes)
    relationships: dict[str, Any] = Field(default_factory=dict)

    @property
    def title(self) -> str:
        return self.attributes.title

    @property
    def state(self) -> str:
        return self.attributes.state

    @property
    def suite_id(self) -> str | None:
        return self.attributes.suite_id

    @property
    def description(self) -> str | None:
        return self.attributes.description

    @property
    def priority(self) -> str | None:
        return self.attributes.priority

    @property
    def tags(self) -> list[str]:
        return self.attributes.tags

    @property
    def assigned_to(self) -> str | None:
        return self.attributes.assigned_to

    @property
    def public_title(self) -> str | None:
        return self.attributes.public_title

    def get_url(self, project_id: str) -> str:
        return f"/projects/{project_id}/tests/{self.id}"


class TestResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: Test
