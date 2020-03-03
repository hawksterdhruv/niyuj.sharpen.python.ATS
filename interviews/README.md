#Install dependencies
pip3 install flask flask_cors sqlalchemy pymysql flask_cors

# Run interview service
python3 interview_app.py

# Add dummy data in job_has_candidate
ALTER TABLE job_has_candidate DROP FOREIGN KEY fk1_job_has_candidate;
ALTER TABLE job_has_candidate DROP FOREIGN KEY fk2_job_has_candidate;
INSERT INTO job_has_candidate(id,candidate_id,position_id) VALUES (1,1,1)
