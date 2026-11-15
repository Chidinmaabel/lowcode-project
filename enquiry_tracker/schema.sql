CREATE TABLE IF NOT EXISTS enquiry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL CHECK (length(customer_name) <= 200),
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    service_type TEXT,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'new'
        CHECK (status IN ('new', 'contacted', 'quote_sent', 'accepted', 'lost')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    follow_up_date TEXT
);