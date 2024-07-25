from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class LabProfileModel(Base):
    __tablename__ = "lab_profiles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String)
    descriptive_title = Column(String)
    course_level = Column(String)
    lab_type = Column(String)
    additional_image = Column(String, nullable=True)
    learning_objectives = relationship("LearningObjectiveModel", back_populates="lab_profile")
    learning_outcomes = relationship("LearningOutcomeModel", back_populates="lab_profile")

class LearningObjectiveModel(Base):
    __tablename__ = "learning_objectives"

    id = Column(Integer, primary_key=True, index=True)
    header = Column(String)
    content = Column(String)
    lab_profile_id = Column(Integer, ForeignKey("lab_profiles.id"))
    lab_profile = relationship("LabProfileModel", back_populates="learning_objectives")

class LearningOutcomeModel(Base):
    __tablename__ = "learning_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    header = Column(String)
    content = Column(String)
    lab_profile_id = Column(Integer, ForeignKey("lab_profiles.id"))
    lab_profile = relationship("LabProfileModel", back_populates="learning_outcomes")

class ConfigureModel(Base):
    __tablename__ = "configures"

    id = Column(Integer, primary_key=True, index=True)
    validity_days = Column(Integer)
    credit_limit = Column(String)
    hour_limit = Column(Integer)
    snooze_lab_start = Column(String)
    snooze_lab_end = Column(String)

class PermissionPolicyModel(Base):
    __tablename__ = "permission_policies"

    id = Column(Integer, primary_key=True, index=True)
    skill_tag = Column(String)
    permission_policy = Column(String)
    allow_programmatic_signup = Column(Boolean)
