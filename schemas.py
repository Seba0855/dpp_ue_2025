from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class MovieBase(BaseModel):
    title: str
    genres: Optional[str] = None


class MovieCreate(MovieBase):
    movieId: int


class MovieUpdate(MovieBase):
    pass


class Movie(MovieBase):
    movieId: int
    model_config = ConfigDict(from_attributes=True)


class LinkBase(BaseModel):
    imdbId: Optional[str] = None
    tmdbId: Optional[str] = None


class LinkCreate(LinkBase):
    movieId: int


class LinkUpdate(LinkBase):
    pass


class Link(LinkBase):
    movieId: int
    model_config = ConfigDict(from_attributes=True)


class RatingBase(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: Optional[int] = None


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    userId: Optional[int] = None
    movieId: Optional[int] = None
    rating: Optional[float] = None
    timestamp: Optional[int] = None


class Rating(RatingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TagBase(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: Optional[int] = None


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    userId: Optional[int] = None
    movieId: Optional[int] = None
    tag: Optional[str] = None
    timestamp: Optional[int] = None


class Tag(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# User schemas
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    roles: Optional[List[str]] = []


class UserResponse(UserBase):
    id: int
    roles: List[str]
    model_config = ConfigDict(from_attributes=True)


class LoginData(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserDetails(BaseModel):
    username: str
    roles: List[str]
