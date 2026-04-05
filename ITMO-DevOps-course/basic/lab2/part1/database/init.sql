CREATE TABLE IF NOT EXISTS votes (
    animal_type VARCHAR(50) PRIMARY KEY,
    votes_count INTEGER DEFAULT 0
);


INSERT INTO votes VALUES ("cats"), ("dogs"), ("giraffe") ON CONFLICT (animal_type) DO NOTHING;