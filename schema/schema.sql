-- CREATE DATABASE IF NOT EXISTS idap;
-- USE idap;

-- CREATE TABLE documents (
--     id BIGINT AUTO_INCREMENT PRIMARY KEY,
--     doc_uuid VARCHAR(64) UNIQUE,
--     filename VARCHAR(255),
--     file_type VARCHAR(50),
--     vision_required BOOLEAN,
--     status VARCHAR(30),
--     reason VARCHAR(255),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

CREATE TABLE documents (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    -- unique document id
    doc_uuid CHAR(36) NOT NULL,

    -- original file info
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,

    -- duplicate detection
    file_hash CHAR(64) NOT NULL,   -- SHA-256

    -- processing flags
    vision_required BOOLEAN DEFAULT FALSE,
    status VARCHAR(30) NOT NULL,
    reason VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- constraints
    UNIQUE KEY uk_doc_uuid (doc_uuid),
    UNIQUE KEY uk_file_hash (file_hash),

    -- performance
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;

CREATE TABLE document_results (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    doc_uuid VARCHAR(64),
    
    doc_category VARCHAR(50),         -- invoice / warranty / feedback / support_ticket
    assigned_team VARCHAR(50),        -- Finance / Warranty / Support / Feedback
    processing_stage VARCHAR(30),     -- rule_based | vision | llm | manual_review
    
    entities JSON,                    -- extracted entities
    missing_fields JSON,              -- fields not found
    
    confidence_score DECIMAL(5,2),    -- used later in LLM phase
    automation_decision VARCHAR(30),  -- auto / human_in_loop / manual_review
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_doc_uuid
        FOREIGN KEY (doc_uuid) REFERENCES documents(doc_uuid)
        ON DELETE CASCADE
);

