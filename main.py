from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import LabProfileModel, ConfigureModel, PermissionPolicyModel, LearningObjectiveModel, LearningOutcomeModel
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum
import logging

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class CategoryEnum(str, Enum):
    category_1 = "python"
    category_2 = "c++"
    category_3 = "cloud"

class CourseLevelEnum(str, Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"

class LabTypeEnum(str, Enum):
    type_1 = "Type 1"
    type_2 = "Type 2"
    type_3 = "Type 3"

class LearningObjective(BaseModel):
    header: str
    content: str

class LabProfile(BaseModel):
    title: str
    category: CategoryEnum
    descriptive_title: str
    course_level: CourseLevelEnum
    lab_type: LabTypeEnum
    additional_image: Optional[str] = None
    learning_objectives: List[LearningObjective]
    learning_outcomes: List[LearningObjective]

class Configure(BaseModel):
    validity_days: int
    credit_limit: str
    hour_limit: int
    snooze_lab_start: str
    snooze_lab_end: str
    

    @validator('validity_days')
    def check_validity_days(cls, v):
        if v <= 0:
            raise ValueError('validity_days must be greater than 0')
        return v

    @validator('hour_limit')
    def check_hour_limit(cls, v):
        if v < 0:
            raise ValueError('hour_limit must be 0 or greater')
        return v

class PermissionPolicy(BaseModel):
    skill_tag: str
    permission_policy: str
    allow_programmatic_signup: bool

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to root page. head towards 127.0.0.1:8000/docs to test API's"}

@app.post("/create_lab_profile/")
async def create_lab_profile(lab_profile: LabProfile, db: Session = Depends(get_db)):
    db_lab_profile = LabProfileModel(
        title=lab_profile.title,
        category=lab_profile.category.value,
        descriptive_title=lab_profile.descriptive_title,
        course_level=lab_profile.course_level.value,
        lab_type=lab_profile.lab_type.value,
        additional_image=lab_profile.additional_image
    )
    db.add(db_lab_profile)
    db.commit()
    db.refresh(db_lab_profile)

    for obj in lab_profile.learning_objectives:
        db_objective = LearningObjectiveModel(
            header=obj.header,
            content=obj.content,
            lab_profile_id=db_lab_profile.id
        )
        db.add(db_objective)

    for outcome in lab_profile.learning_outcomes:
        db_outcome = LearningOutcomeModel(
            header=outcome.header,
            content=outcome.content,
            lab_profile_id=db_lab_profile.id
        )
        db.add(db_outcome)

    db.commit()
    return db_lab_profile

@app.get("/lab_profiles/")
async def get_lab_profiles(db: Session = Depends(get_db)):
    try:
        lab_profiles = db.query(LabProfileModel).all()
        print(f"Lab Profiles: {lab_profiles}") 
        return lab_profiles
    except Exception as e:
        logging.error(f"Error fetching lab profiles: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/create_configure/")
async def create_configure(configure: Configure, db: Session = Depends(get_db)):
    db_configure = ConfigureModel(
        validity_days=configure.validity_days,
        credit_limit=configure.credit_limit,
        hour_limit=configure.hour_limit,
        snooze_lab_start=configure.snooze_lab_start,
        snooze_lab_end=configure.snooze_lab_end
        
    )
    db.add(db_configure)
    db.commit()
    db.refresh(db_configure)
    return db_configure

@app.get("/configures/")
async def get_configures(db: Session = Depends(get_db)):
    try:
        configures = db.query(ConfigureModel).all()
        return configures
    except Exception as e:
        logging.error(f"Error fetching configures: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/create_permission_policy/")
async def create_permission_policy(permission_policy: PermissionPolicy, db: Session = Depends(get_db)):
    db_permission_policy = PermissionPolicyModel(
        skill_tag=permission_policy.skill_tag,
        permission_policy=permission_policy.permission_policy,
        allow_programmatic_signup=permission_policy.allow_programmatic_signup
    )
    db.add(db_permission_policy)
    db.commit()
    db.refresh(db_permission_policy)
    return db_permission_policy

@app.get("/permission_policies/")
async def get_permission_policies(db: Session = Depends(get_db)):
    try:
        permission_policies = db.query(PermissionPolicyModel).all()
        return permission_policies
    except Exception as e:
        logging.error(f"Error fetching permission policies: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
