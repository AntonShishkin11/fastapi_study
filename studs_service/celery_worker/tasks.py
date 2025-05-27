from celery import shared_task
from database.sync_session import SessionLocal
from database.models import Students
import pandas as pd

@shared_task
def import_csv_task(csv_path: str):
    session = SessionLocal()
    try:
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            student = Students(
                last_name=row["last_name"],
                first_name=row["first_name"],
                faculty=row["faculty"],
                course=row["course"],
                mark=int(row["mark"])
            )
            session.add(student)
        session.commit()
        return f"Imported {len(df)} students from {csv_path}"
    except Exception as e:
        session.rollback()
        return f"Error importing CSV: {str(e)}"
    finally:
        session.close()

@shared_task
def delete_students_task(ids: list[int]):
    session = SessionLocal()
    try:
        deleted = session.query(Students).filter(Students.id.in_(ids)).delete(synchronize_session=False)
        session.commit()
        return f"Deleted {deleted} students with IDs {ids}"
    except Exception as e:
        session.rollback()
        return f"Error deleting students: {str(e)}"
    finally:
        session.close()
