# User Profile & Goals
CREATE TABLE user_profile (
    id INT PRIMARY KEY DEFAULT 1,
    goal_calories INT DEFAULT 2000,
    next_day_goal INT DEFAULT 2000,
    current_weight FLOAT
);

# Insert default profile row to ensure updates work
INSERT INTO user_profile (id, goal_calories, next_day_goal, current_weight) VALUES (1, 2000, 2000, NULL) ON CONFLICT DO NOTHING;

-- Daily Logs (Automated reset at 00:00 - handled by app filtering)
CREATE TABLE food_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    label TEXT NOT NULL,
    calories INT NOT NULL,
    emoji TEXT,
    raw_ai_suggestion JSONB
);

-- Weight Tracking
CREATE TABLE weight_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    recorded_at DATE DEFAULT CURRENT_DATE,
    weight_value FLOAT NOT NULL
);
