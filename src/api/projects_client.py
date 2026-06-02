from dataclasses import dataclass

import requests


@dataclass
class ProjectAttributes:
    title: str
    url: str | None
    slug: str | None
    description: str | None
    private: bool
    enabled: bool
    status: str | None
    tests_count: int | None
    created_at: str | None
    updated_at: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectAttributes":
        return cls(
            title=data["title"],
            url=data.get("testomatio-url"),
            slug=data.get("slug"),
            description=data.get("description"),
            private=data.get("private", False),
            enabled=data.get("enabled", True),
            status=data.get("status"),
            tests_count=data.get("tests-count"),
            created_at=data.get("created-at"),
            updated_at=data.get("updated-at"),
        )


@dataclass
class Project:
    id: str
    type: str
    attributes: ProjectAttributes

    @property
    def url(self) -> str | None:
        return self.attributes.url

    @property
    def slug(self) -> str | None:
        return self.attributes.slug

    @property
    def title(self) -> str:
        return self.attributes.title

    @property
    def status(self) -> str | None:
        return self.attributes.status

    @property
    def tests_count(self) -> int | None:
        return self.attributes.tests_count

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        return cls(
            id=data["id"],
            type=data["type"],
            attributes=ProjectAttributes.from_dict(data["attributes"]),
        )


@dataclass
class ProjectsResponse:
    data: list[Project]
    status_code: int
    headers: dict
    url: str

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    @classmethod
    def from_response(cls, response: requests.Response) -> "ProjectsResponse":
        data = []
        if response.ok:
            data = [Project.from_dict(item) for item in response.json().get("data", [])]
        return cls(
            data=data,
            status_code=response.status_code,
            headers=dict(response.headers),
            url=response.url,
        )


class ProjectsClient:
    def __init__(self, base_url: str, api_token: str):
        self._base_url = base_url
        self._session = requests.Session()
        jwt = self._login(api_token)
        self._session.headers.update({"Authorization": jwt})

    def _login(self, api_token: str) -> str:
        response = self._session.post(
            f"{self._base_url}/api/login",
            json={"api_token": api_token},
        )
        response.raise_for_status()
        return response.json()["jwt"]

    def get_projects(self) -> ProjectsResponse:
        return ProjectsResponse.from_response(self._session.get(f"{self._base_url}/api/projects"))

    @classmethod
    def unauthorized(cls, base_url: str) -> "ProjectsClient":
        instance = object.__new__(cls)
        instance._base_url = base_url
        instance._session = requests.Session()
        instance._session.headers.update({"Authorization": "invalid_token"})
        return instance
